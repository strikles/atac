from operator import truediv
import os
import random
import sys
import pytest
import atac

# :(
emergency = True
#
encrypted_config = False
config_file = 'auth.json'
key_file = None


emergency_subjects = [
    "jasper kums and colégio militar alumni gamble with life and direct violence inducing synthetic psychosis in the middle of the night, abusing biophotonics to direct violence against parents, women and children",
    "colégio militar alumni and criminal associates participate in interactive human degradation spectacles to turn people homeless, force them into poverty, gambling life in blue whale suicide games where they take turns abusing biophotonics to execute vibrotactile cybertorture, force psychosis and simulate Van Gogh syndrome in a style reminiscent of the murder of Matthew Puncher"
]

development_subjects = [
    "abuse of biophotonics to execute cybertorture and force victims to complete tasks as a way to bargain for relief",
]

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
subjects = development_subjects

if emergency == True:
    recipients = emergency_recipients
    email_file = emergency_email_file
    subjects = emergency_subjects

target_languages = ['el', 'fr', 'it', 'ja', 'pt', 'uk', 'nl', 'la']




@pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    #
    katie = atac.SendEmail(encrypted_config, config_file, key_file)
    auth, _ = katie.get_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    print(os.path.abspath(os.getcwd()))
    mailing_list = "; ".join(recipients)
    status = katie.send(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode=None)
    assert(status == 0) is True


@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_translation():
    """
    """
    #
    katie = atac.SendEmail(encrypted_config, config_file, key_file)
    auth, _ = katie.get_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send(mailing_list, message_content, subject, do_paraphrase=False, translate_to_languagecode="pt")
    assert(status == 0) is True


@pytest.mark.skip(reason="we fight spam :)")
def test_send_email_with_paraphrase():
    """
    """
    #
    katie = atac.SendEmail(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    #
    subject = random.sample(subjects, 1).pop()
    message_content = katie.get_file_content(os.path.abspath(os.path.join(os.getcwd(), "data/messages/email/neurorights.md")), "message")
    mailing_list = random.sample(recipients, 1).pop()
    status = katie.send(mailing_list, message_content, subject, do_paraphrase=True, translate_to_languagecode=None)
    assert(status == 0) is True


@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails_with_paraphrasing_and_translation():
    """
    """
    #
    katie = atac.SendEmail(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), email_file)
    message_file_path = os.path.join(os.getcwd(), "data/messages/email/neurorights.md")
    subject = random.sample(subjects, 1).pop()
    for lang_code in target_languages:
        status = katie.send_batch(email_files_path, message_file_path, subject, True, lang_code)
        assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails_with_no_paraphrasing_and_no_translation():
    """
    """
    #
    katie = atac.SendEmail(encrypted_config, config_file, key_file)
    email_files_path = os.path.join(os.getcwd(), email_file)
    message_file_path = os.path.join(os.getcwd(), "data/messages/email/neurorights.md")
    subject = random.sample(subjects, 1).pop()
    status = katie.send_batch(email_files_path, message_file_path, subject, False, None)
    assert(status == 0) is True