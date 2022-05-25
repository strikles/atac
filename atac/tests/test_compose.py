import pytest
import os
import requests
from requests import HTTPError
import sys

import atac

encrypted_config = False
config_file = "auth.json"
key_file = None


@pytest.mark.skip(reason="refactoring :)")
def test_markov():
    """
    Generates encryption key from password + salts

    Parameters
    ----------
    name : str
        The name of the animal
    sound : str
        The sound the animal makes
    num_legs : int, optional
        The number of legs the animal (default is 4)
    """

    response = None
    try:
        url = "https://raw.githubusercontent.com/jsvine/markovify/master/test/texts/sherlock.txt"
        response = requests.get(url, timeout=10, stream=False)
        response.encoding = "utf-8"
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    #
    two_back = atac.Compose(encrypted_config, config_file, key_file)
    assert (len(two_back.generate_markov_content(response.text)) < 200) is True
