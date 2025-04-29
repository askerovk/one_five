"""ETL dag for parsing json files and populating clickhouse DB."""
import glob
import os
import pendulum

from docker.types import Mount
import clickhouse_connect
from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator



os.chdir('/opt/airflow/dags')


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def data_processing():
    """Main ETL dag."""
    @task()
    def get_pending_json_paths():
        json_paths = glob.glob('/opt/airflow/data/texts/*.json')

        client = clickhouse_connect.get_client(
            host='clickhouse',
            username=os.environ['CLICKHOUSE_USER'],
            password=os.environ['CLICKHOUSE_PASSWORD'])

        processed_paths = client.query_np(
            "SELECT source_path FROM warehouse.dim_sources;"
            )

        processed_paths = [x[0] for x in processed_paths]

        new_paths = list(
            set(json_paths) - set(processed_paths)
        )

        list_range = range(0, len(new_paths), 100)

        json_paths = [new_paths[i:i + 100] for i in list_range]

        result = []

        for path_list in json_paths:

            result.append({
                'CLICKHOUSE_USER': os.environ['CLICKHOUSE_USER'],
                'CLICKHOUSE_PASSWORD': os.environ['CLICKHOUSE_PASSWORD'],
                'JSON_PATHS': path_list
            })

        return result

    env_override_list = get_pending_json_paths()

    DockerOperator.partial(
        task_id='parse_pending_jsons',
        image='data_processing',
        mounts=[Mount(
            source=os.environ['PROJECT_DIR_PATH'] + '/data_processing/data/',
            target="/opt/airflow/data/", type="bind")
        ],
        docker_url="unix://var/run/docker.sock",
        network_mode='one_five_project',
        auto_remove='success',
        mount_tmp_dir=False,
        max_active_tis_per_dag=5
    ).expand(environment=env_override_list)


data_processing()
