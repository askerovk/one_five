"""Utility functions for reading and tokenizing texts."""
import json
import uuid
import re
import string

from nltk.tokenize import TreebankWordTokenizer


def get_raw_texts(json_paths):
    """Parse json and enrich json files.
    Params:
        (list): relative paths to json files
    Returns:
        (list): list of dictionaries

    """
    result = []

    # Parse json files
    for path in json_paths:
        with open(path, "r") as json_file:
            json_data = json.load(json_file)

        # Add json relative path
        json_data["source_path"] = path

        # Generate data source id
        json_data["source_id"] = str(uuid.uuid4())

        result.append(json_data)

    return result


def tokenize_text(text):
    """Split a body of text into word tokens.
    Params:
        (str) text corpus
    Returns:
        (list) list of word tokens
    """
    tokens = TreebankWordTokenizer().tokenize(text)

    # Remove punctuation marks
    tokens = [word for word in tokens if word not in string.punctuation]

    # Convert words to lowercase
    tokens = [word.lower() for word in tokens]

    # Remove trailing dots on certain words
    tokens = [re.sub("\\.$", "", word) for word in tokens]

    return tokens
