import os

import clickhouse_connect

from utils import get_raw_texts
from create_df import (
    create_dim_sources,
    create_token_df,
    create_dim_words,
    create_word_counts,
)
from upload import upload_dim_sources, upload_dim_words, upload_fact_words_counts


def app():
    client = clickhouse_connect.get_client(
        host="clickhouse", username="admin", password=os.environ["CLICKHOUSE_PASSWORD"]
    )

    json_paths = os.environ["JSON_PATHS"]

    raw_texts = get_raw_texts(json_paths=json_paths)

    dim_sources = create_dim_sources(raw_texts)

    upload_dim_sources(client=client, dim_sources=dim_sources)

    token_df = create_token_df(raw_texts)

    dim_words = create_dim_words(token_df=token_df)

    upload_dim_words(client=client, dim_sources=dim_words)

    fact_word_counts = create_word_counts(token_df=token_df)

    upload_fact_words_counts(client=client, fact_word_counts=fact_word_counts)


if __name__ == "__main__":
    app.py()
