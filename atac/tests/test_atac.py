import os
import sys
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


def test_markov():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    content = dir_path + '/assets/pg1009.txt'
    two_back = atac.AllTimeHigh()
    assert(two_back.gen_content(content)) == 0


def test_invalid_url():
    mango = atac.UnderTheMangoTree(encrypted_config, config_file, key_file)
    url1 = ""
    assert(mango.invalid_url(url1)) is False
    url2 = "www.google.com"
    assert(mango.invalid_url(url2)) is True
    url3 = "strikles@gmail.com"
    assert(mango.invalid_url(url3)) is False


def test_extract_emails():
    mango = atac.UnderTheMangoTree(encrypted_config, config_file, key_file)
    content = "me@gmail.com, you@yahoo.com"
    new_emails = mango.extract_emails(content)
    expected = set()
    expected.update({'me@gmail.com'})
    expected.update({'you@yahoo.com'})
    assert(new_emails == expected) is True


def test_extract_phones():
    mango = atac.UnderTheMangoTree(encrypted_config, config_file, key_file)
    content = "+351 99999999, +31 45678541"
    new_phones = mango.extract_phones(content)
    expected = set()
    expected.update({'+351 99999999'})
    expected.update({'+31 45678541'})
    assert(new_phones == expected) is True


def test_process_page():
    mango = atac.UnderTheMangoTree(encrypted_config, config_file, key_file)
    status = mango.process_page("test", "https://raw.githubusercontent.com/strikles/atac/main/SCRAPEME.md")
    assert(status) == 0
