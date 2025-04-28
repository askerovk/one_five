import json
import glob
import pendulum

from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator
import clickhouse_connect
from docker.types import Mount



import os
os.chdir('/opt/airflow/dags')

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def data_processing():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """
    @task()
    def generate_json_lists():
        json_paths = glob.glob('/opt/airflow/data/texts/*.json')

        client = clickhouse_connect.get_client(
            host='clickhouse',
            username='admin',
            password=os.environ['CLICKHOUSE_PASSWORD'])

        processed_paths = client.query_np("SELECT source_path FROM warehouse.dim_sources;")

        new_paths = list(
            set(json_paths) - set(list(processed_paths))
        )

        list_range = range(0, len(new_paths), 100)

        json_paths = [new_paths[i:i + 100] for i in list_range]

        result = []

        for path_list in json_paths:

            result.append({
                'CLICKHOUSE_PASSWORD': os.environ['CLICKHOUSE_PASSWORD'],
                'JSON_PATHS': path_list
            })

        return result

    env_override_list = generate_json_lists()

    DockerOperator.partial(
        task_id='process_texts',
        image='data_processing',
        mounts=[
            Mount(source="/home/kamran/Documents/one_five_project/data_processing/data/", target="/opt/airflow/data/", type="bind")
        ],
        docker_url="unix://var/run/docker.sock",
        network_mode='one_five_project',
        auto_remove='success',
        mount_tmp_dir=False,
        max_active_tis_per_dag=3

    ).expand(environment=env_override_list)


data_processing()
