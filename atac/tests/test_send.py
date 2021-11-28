import os
import random
import sys
import pytest
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


@pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    recipients = [
        'civilsociety@ohchr.org',
        'youthenvoy@un.org',
        'education-outreach@un.org',
        'contactnewscentre@un.org',
        'staffunionu@un.org',
        'sssgeneva@un.org',
        'controlcenter.security-unog@un.org',
        'unog.protocol@un.org',
        'unog.political@un.org',
        'unog.ngo@un.org',
        'sdg-lab@un.org',
        'perceptionchange@un.org',
        'procurementunog@un.org',
        'dcmdirector@un.org',
        'unoda-geneva@un.org',
        'press_geneva@un.org',
        'untv@un.org',
        'library-gva@un.org',
        'archives-gva@un.org',
        'museum-gva@un.org',
        'culturelibraryunog@un.org'
    ]
    mailing_list = random.sample(recipients, 1).pop()
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    message_content = u'\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message.md", "message"))
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    katie.send_email(mailing_list, message)


@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails():
    """
    """
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    katie.send_emails(email_files_path, message_file_path, subject)


def test_send_emails_envelope():
    """
    """
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    katie.send_emails_envelope(email_files_path, message_file_path, subject)
