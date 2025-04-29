"""Main app for running the json parsing ETL."""
import os
from ast import literal_eval
import logging

import clickhouse_connect

from utils import get_raw_texts
from create_df import (
    create_dim_sources,
    create_token_df,
    create_dim_words,
    create_word_counts,
)
from upload import upload_dim_sources, upload_dim_words, upload_fact_words_counts

log_formatter = logging.Formatter(
    "{levelname} - {name} - {asctime} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
)
root_logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)
root_logger.setLevel(logging.INFO)


def app():
    """Main, top level function for ETL."""
    root_logger.info("Connecting to clickhouse db.")
    client = clickhouse_connect.get_client(
        host="clickhouse",
        username=os.environ["CLICKHOUSE_USER"],
        password=os.environ["CLICKHOUSE_PASSWORD"]
    )

    root_logger.info("Fetching json paths from env vars.")
    json_paths = literal_eval(os.environ["JSON_PATHS"])

    root_logger.info("Parsing json texts.")
    raw_texts = get_raw_texts(json_paths=json_paths)

    root_logger.info("Building dim_sources.")
    dim_sources = create_dim_sources(raw_texts)

    root_logger.info("Uploading dim_sources.")
    upload_dim_sources(client=client, dim_sources=dim_sources)

    root_logger.info("Building token_df.")
    token_df = create_token_df(raw_texts)

    root_logger.info("Building dim_words.")
    dim_words = create_dim_words(token_df=token_df)

    root_logger.info("Uploading dim_words.")
    upload_dim_words(client=client, dim_sources=dim_words)

    root_logger.info("Building fact_word_counts.")
    fact_word_counts = create_word_counts(token_df=token_df)

    root_logger.info("Uploading fact_word_counts.")
    upload_fact_words_counts(client=client, fact_word_counts=fact_word_counts)

    root_logger.info("Work complete.")


if __name__ == "__main__":
    app()
