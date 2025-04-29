"""Functions which create matching dataframe for clickhouse tables."""
import uuid
from datetime import datetime

import pandas as pd
from nltk.corpus import stopwords

from utils import tokenize_text


def create_dim_sources(raw_inputs):
    """Create a text source dimension data frame.
    Params:
        (list) list of json dictionaries
    Returns:
        (pandas DataFrame)
    """
    dim_sources = pd.DataFrame().from_records(raw_inputs)

    dim_sources.rename(columns={"id": "source_title"}, inplace=True)

    dim_sources.drop(columns=["text"], inplace=True)

    dim_sources["created_at"] = datetime.now()

    return dim_sources


def create_token_df(raw_inputs):
    """Create an intermediary word token dataframe.
    Params:
        (list) list of raw json dicts
    Returns:
        (pandas DataFrame) intermediary token dataframe.
    """
    token_df = pd.DataFrame().from_records(raw_inputs).loc[:, ["source_path", "text"]]

    # Split text into individual tokens
    token_df["text"] = token_df["text"].apply(tokenize_text)

    # Convert list of tokens into rows
    token_df = token_df.explode("text")

    return token_df


def create_dim_words(token_df):
    """Create an a word dimension dataframe.
    Params:
        (pandas DataFrame) intermediary token dataframe
    Returns:
        (pandas DataFrame) dim_words dataframe
    """
    # Get a pandas series of unique words
    dim_words = pd.DataFrame({"word_english": token_df.text.unique()})

    # Generate word ids
    dim_words["word_id"] = dim_words["word_english"].apply(lambda x: str(uuid.uuid4()))

    # Create a flag boolean for stopwords.
    stop_words = set(stopwords.words("english"))

    dim_words["is_stopword"] = dim_words["word_english"].apply(
        lambda x: x in stop_words
    )

    # Add created_at timestamp
    dim_words["created_at"] = datetime.now()

    return dim_words


def create_word_counts(token_df):
    """Create an a word count dataframe.
    Params:
        (pandas DataFrame) intermediary token dataframe
    Returns:
        (pandas DataFrame) fact_words_counts datafame
    """
    # Calculate counts of unique words per text source
    fact_word_counts = token_df.value_counts().reset_index()

    fact_word_counts.rename(columns={"text": "word_english"}, inplace=True)

    # Add created_at timestamp
    fact_word_counts["created_at"] = datetime.now()

    # Generate word count ids
    fact_word_counts["count_id"] = fact_word_counts["count"].apply(
        lambda x: str(uuid.uuid4())
    )

    return fact_word_counts
