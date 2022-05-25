import os
import sys
import atac

encrypted_config = False
config_file = "auth.json"
key_file = None


# @pytest.mark.skip(reason="we fight spam :)")
def test_invalid_url():
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
    mango = atac.Scrape(encrypted_config, config_file, key_file)
    url1 = ""
    assert (mango.invalid_url(url1)) is False
    url2 = "www.google.com"
    assert (mango.invalid_url(url2)) is True
    url3 = "strikles@gmail.com"
    assert (mango.invalid_url(url3)) is False


# @pytest.mark.skip(reason="we fight spam :)")
def test_extract_emails():
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
    mango = atac.Scrape(encrypted_config, config_file, key_file)
    content = "me@gmail.com, you@yahoo.com"
    new_emails = mango.extract_emails(content)
    expected = set()
    expected.update({"me@gmail.com"})
    expected.update({"you@yahoo.com"})
    assert (new_emails == expected) is True


# @pytest.mark.skip(reason="we fight spam :)")
def test_extract_phones():
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
    mango = atac.Scrape(encrypted_config, config_file, key_file)
    content = "+351 99999999, +31 45678541"
    new_phones = mango.extract_phones(content)
    expected = set()
    expected.update({"+351 99999999"})
    expected.update({"+31 45678541"})
    assert (new_phones == expected) is True


# @pytest.mark.skip(reason="we fight spam :)")
def test_process_page():
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
    mango = atac.Scrape(encrypted_config, config_file, key_file)
    status = mango.process_page(
        "test", "https://letterhub.com/wp-content/uploads/2018/03/100-contacts.csv"
    )
    assert (status) == 0
