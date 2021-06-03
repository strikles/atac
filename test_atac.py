import os, sys
import atac

def test_markov():
    content = os.path.dirname(os.path.abspath(__file__)) + '/assets/pg1009.txt'
    two_back = atac.AllTimeHigh()
    assert(two_back.gen_content(content)) == 0

"""
def test_email():
    katie = FromRuXiaWithLove()
    assert(katie.send_email()) == 0
"""

"""
def test_facebook():
    katie = FromRuXiaWithLove()
    assert(katie.send_facebook()) == 0
"""

"""
def test_twitter():
    katie = FromRuXiaWithLove()
    assert(katie.send_twitter()) == 0
"""
    
"""
def test_whatsapp():
    katie = FromRuXiaWithLove()
    assert(katie.send_whatsapp()) == 0
"""

def test_invalid_url():
    mango = atac.UnderTheMangoTree()
    url1 = ""
    assert(mango.invalid_url(url1)) == False
    url2 = "www.google.com"
    assert(mango.invalid_url(url2)) == True
    url3 = "strikles@gmail.com"
    assert(mango.invalid_url(url3)) == False

def test_extract_emails():
    mango = atac.UnderTheMangoTree()
    content = "me@gmail.com, you@yahoo.com"
    new_emails = mango.extract_emails(content)
    expected = set()
    expected.update({'me@gmail.com'})
    expected.update({'you@yahoo.com'})
    assert(new_emails == expected) == True

def test_extract_phones():
    mango = atac.UnderTheMangoTree()
    content = "+351 99999999, +31 45678541"
    new_phones = mango.extract_phones(content)
    expected = set()
    expected.update({'+351 99999999'})
    expected.update({'+31 45678541'})
    assert(new_phones == expected) == True
    
"""
def test_save_emails():
"""

"""
def test_save_phones():
"""

def test_process_page():
    mango = atac.UnderTheMangoTree()
    status = mango.process_page("test", "https://raw.githubusercontent.com/strikles/atac/main/assets/SCRAPEME.md")
    assert(status) == 0


