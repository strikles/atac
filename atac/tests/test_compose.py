import os
import sys
import requests
from requests import HTTPError
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


def test_markov():
    #
    response = None
    try:
        url = "https://raw.githubusercontent.com/jsvine/markovify/master/test/texts/sherlock.txt"
        response = requests.get(url, timeout=10, stream=False)
        response.encoding = "utf-8"
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        continue
    except Exception as err:
        print(f'Other error occurred: {err}')
        continue
    else:
        pass
    #
    two_back = atac.AllTimeHigh(encrypted_config, config_file, key_file)
    assert(len(two_back.generate_markov_content(response.text)) < 200) is True
