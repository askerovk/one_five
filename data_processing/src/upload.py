"""Function which upload dataframe data to clickhouse."""
import uuid
import re


def upload_dim_sources(client, dim_sources):
    """Upload the dim_sources data frame to clickhouse.
    Params:
        (clickchouse client)
        (pandas DataFrame)
    Returns:
        None
    """
    # Create a temporary table
    table_name = 'temp.' + re.sub("-", "", str(uuid.uuid4()))

    query_1 = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        source_id varchar(50) ,
        source_title varchar(100),
        source_path varchar(200),
        created_at timestamp,
        updated_at timestamp,
        deleted_at timestamp,
        PRIMARY KEY(source_id)
    )"""

    client.command(query_1)

    # Upload data frame to temporary table
    client.insert_df(table=table_name, df=dim_sources)

    # Insert only the rows, who's file paths are not found in
    # warehouse.dim_sources
    query_2 = f"""
    INSERT INTO warehouse.dim_sources
    SELECT A.* FROM {table_name} A
    LEFT ANTI JOIN warehouse.dim_sources B
    ON A.source_path = B.source_path;
    """

    client.command(query_2)

    # Drop temporary table
    client.command(f"DROP TABLE {table_name}")

    return None


def upload_dim_words(client, dim_sources):
    """Upload the dim_words data frame to clickhouse.
    Params:
        (clickchouse client)
        (pandas DataFrame)
    Returns:
        None
    """
    # Create a temporary table
    table_name = 'temp.' + re.sub("-", "", str(uuid.uuid4()))

    query_1 = f"""CREATE TABLE IF NOT EXISTS {table_name} (
        word_id varchar(50),
        word_english varchar(100),
        is_stopword boolean,
        created_at timestamp,
        updated_at timestamp,
        deleted_at timestamp,
        PRIMARY KEY(word_id)
    )"""

    client.command(query_1)

    # Upload data frame to temporary table
    client.insert_df(table=table_name, df=dim_sources)

    # Insert only the rows, who's word ids are not found in
    # warehouse.dim_words
    query_2 = f"""
        INSERT INTO warehouse.dim_words
        SELECT A.* FROM {table_name} A
        LEFT ANTI JOIN warehouse.dim_words B
        ON A.word_english = B.word_english;
    """

    client.command(query_2)

    # Drop temporary table
    client.command(f"DROP TABLE {table_name}")

    return None


def upload_fact_words_counts(client, fact_word_counts):
    """Upload the fact_word_counts data frame to clickhouse.
    Params:
        (clickchouse client)
        (pandas DataFrame)
    Returns:
        None
    """
    # Create a temporary table
    table_name = 'temp.' + re.sub("-", "", str(uuid.uuid4()))

    query_1 = f"""CREATE TABLE IF NOT EXISTS {table_name} (
    count_id varchar(50),
    source_path varchar(50),
    word_english varchar(50),
    count int,
    created_at timestamp,
    updated_at timestamp,
    deleted_at timestamp,
    PRIMARY KEY(count_id)
    )"""

    client.command(query_1)

    # Upload data frame to temporary table
    client.insert_df(table=table_name, df=fact_word_counts)

    # Replace words with word ids, source names with source ids
    # and, upload word counts to fact_word_counts
    query_2 = f"""
        INSERT INTO warehouse.fact_word_counts
        SELECT
            count_id,
            B.source_id,
            C.word_id,
            count,
            A.created_at AS created_at,
            A.updated_at AS updated_At,
            A.deleted_at AS deleted_at
        FROM {table_name} A
        LEFT JOIN warehouse.dim_sources B
        ON A.source_path = B.source_path
        LEFT JOIN warehouse.dim_words C
        ON A.word_english = C.word_english;
    """

    client.command(query_2)

    # Drop temporary table
    client.command(f"DROP TABLE {table_name}")

    return None
