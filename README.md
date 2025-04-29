## Technical Task for one.five

### Architecture

A lucid chart diagram of the project, ETL code step algorithm and Clickhouse ERD diagram can be viewed [here](https://drive.google.com/file/d/1ecpWdGnjPuWEd6hfoA_cZcUHxpScmsrn/view?usp=sharing) (click on 'Open with draw.io').

This project has the following components:
* An instance of Apache Airflow as an ETL orchestrator.
* An instance of Clickhouse Database, which houses the data warehouse, datamart and sandbox.
* An instance of PrestoDB, as a SQL query engine.
* A dockerized ETL script.

### Setup Instructions

1. Unzip the ‘project.zip’ archive into your local machine.
2. Open terminal and navigate to the 'one_five_project' directory.
3. Run the following commands in the terminal:
```
export PROJECT_DIR_PATH=$(pwd)
docker compose build
docker compose up airflow-init
docker compose up -d
```

### Resource access.

1. Airflow:
* The webserver is hosted on 'http://localhost:8080/'.
* It is accessible with default credentials ('admin' for both username and password)
2. Clickhouse database:
* The database can be accessed with DBeaver application (free community edition). 
* When setting up a connection: Host: localhost | Port: 8123. Leave the database field blank. (jdbc:clickhouse://localhost:8123)
* You have 3 options for users:
1. User 'admin', password 'password1' - full database access.
2. User 'airflow', password 'password2' - read/write access, ability to create and drop tables in 'temp' database. Not intended for human users.
3. User 'analyst', password 'password3' - read only access to 'warehouse' and 'datamart' databases, full privileges on 'analytics_sandbox' database.
3. PrestoDB:
* The database query engine can be accessed with DBeaver application (free community edition).
* When setting up a connection: Host: localhost | Port: 8081. Leave the database field blank. (jdbc:presto://localhost:8081)
* Currently accessed with user 'root', leave password field blank.

### Running the ETL

1. Login to airflow, navigate to the data_processing dag and trigger it manually.
2. The dag will populate tables in warehouse database on clickhouse db. The datamart tables will be populated by clickhouse materialized views. 
