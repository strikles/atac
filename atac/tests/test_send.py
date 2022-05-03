import os
import random
import sys
import pytest
import atac

encrypted_config = False
config_file = 'auth.json'
key_file = None

recipients = [
    'contacto@psp.pt',
    'geral@prociv.pt',
    'gnr@gnr.pt',
    'mail@ansr.pt',
    'sef@sef.pt',
    'geral@igai.pt',
    'sec.geral.mai@sg.mai.gov.pt',
    'geral@igai.pt'
]
#
target_languages = ['el', 'fr', 'it', 'ja', 'pt', 'uk', 'nl', 'la']
#
subjects = [
        "<span translate='no'>jasper kums</span> and <span translate='no'>colégio militar</span> alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night, abusing <span translate='no'>biophotonics</span> to direct violence against parents, women and children",
        "abusing <span translate='no'>biophotonics</span> for <span translate='no'>cybertorture</span> in order to force the victims to complete tasks to bargain for relief",
        "<span translate='no'>colégio_militar</span> alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in <span translate='no'>blue whale</span> suicide games where they take turns abusing <span translate='no'>biophotonics</span> to execute vibrotactile <span translate='no'>cybertorture</span>, force psychosis and simulate <span translate='no'>Van Gogh</span> syndrome in a style reminiscent of the murder of <span translate='no'>Matthew Puncher</span>"
]

#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = "; ".join(recipients)
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode=None)
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_translation():
    """
    """
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode="pt")
    assert(status == 0) is True


@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_paraphrase():
    """
    """
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send_email(mailing_list, message_content, subject, do_paraphrase=True, translate_to_languagecode=None)
    assert(status == 0) is True


@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails_with_paraphrasing_and_translation():
    """
    """
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), "atac/tests/contacts/test_emails.csv")
    #
    for lang_code in target_languages:
        #
        message_file_path = os.path.join(os.getcwd(), "data/messages/email/neurorights.md")
        subject = random.sample(subjects, 1).pop()
        status = katie.send_emails(email_files_path, message_file_path, subject, True, lang_code)
        assert(status == 0) is True
