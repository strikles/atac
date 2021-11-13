import os
import sys
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


def test_markov():
    path = os.path.abspath('..')
    content = path + '/atac/assets/pg1009.txt'
    two_back = atac.AllTimeHigh(None, None, None, None)
    assert(two_back.gen_content(content)) == 0
