import os
import sys
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


def test_markov():
    path = os.path.abspath('..')
    content = path + '/atac/data/pg1009.txt'
    two_back = atac.AllTimeHigh(encrypted_config, config_file, key_file)
    assert(len(two_back.generate_markov_content(content)) < 200) is True
