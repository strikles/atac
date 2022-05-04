import os
import random
import sys
import pytest
import atac

# :(
emergency = False
#
encrypted_config = False
config_file = 'auth.json'
key_file = None

emergency_recipients = [
    'contacto@psp.pt',
    'geral@prociv.pt',
    'gnr@gnr.pt',
    'mail@ansr.pt',
    'sef@sef.pt',
    'geral@igai.pt',
    'sec.geral.mai@sg.mai.gov.pt',
    'geral@igai.pt'
]

development_recipients = [
    "strikles@gmail.com",
    "opvs.minor@gmail.com",
    "benedictvs.ora.labora@gmail.com"
]


emergency_email_file = "atac/tests/contacts/emergency_used_only_whilst_under_torture.csv"
development_email_file = "atac/tests/contacts/test_development.csv"

recipients = development_recipients
email_file = development_email_file

if emergency == True:
    recipients = emergency_recipients
    email_file = emergency_email_file

target_languages = ['el', 'fr', 'it', 'ja', 'pt', 'uk', 'nl', 'la']

subjects = [
        "<span translate='no'>jasper kums</span> and <span translate='no'>colégio militar</span> alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night, abusing <span translate='no'>biophotonics</span> to direct violence against parents, women and children",
        "abuse of <span translate='no'>biophotonics</span> to execute <span translate='no'>cybertorture</span> and force victims to complete tasks as a way to bargain for relief",
        "<span translate='no'>colégio_militar</span> alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in <span translate='no'>blue whale</span> suicide games where they take turns abusing <span translate='no'>biophotonics</span> to execute vibrotactile <span translate='no'>cybertorture</span>, force psychosis and simulate <span translate='no'>Van Gogh</span> syndrome in a style reminiscent of the murder of <span translate='no'>Matthew Puncher</span>"
]


@pytest.mark.skip(reason="we fight spam :)")
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


@pytest.mark.skip(reason="we fight spam :)")
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


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails_with_no_paraphrasing_and_no_translation():
    """
    """
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), email_file)
    message_file_path = os.path.join(os.getcwd(), "data/messages/email/neurorights.md")
    subject = random.sample(subjects, 1).pop()
    status = katie.send_emails(email_files_path, message_file_path, subject, False, 'en')
    assert(status == 0) is True
    """
    for lang_code in target_languages:
        status = katie.send_emails(email_files_path, message_file_path, subject, False, lang_code)
    """
