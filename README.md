# Word count project
The following python project processes texts from json files and loads the raw data into the data warehouse

## Local environment without docker
We need to set up poetry to load the ENV variables automatically.
```shell
pip install poetry==1.7.1 && poetry install
```
We add the plugin for .env load
```shell
poetry self add poetry-dotenv-plugin
```
Then we run the job
```shell
poetry run python -m src.main
```

## Docker deployment (Local machine)
Dependencies:
- Docker & Docker-compose

To build the docker compose images
```shell
docker-compose build
```
To run all the images and execute the entrypoint.sh (to automatically run the python code)
```shell
docker-compose up
```

