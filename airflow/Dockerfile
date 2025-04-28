FROM apache/airflow:2.10.5

COPY ./requirements.txt /usr/local/requirements.txt

RUN pip install --no-cache-dir apache-airflow==2.10.5 -r /usr/local/requirements.txt