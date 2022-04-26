import os
import random
import sys
import pytest
import atac


encrypted_config = False
config_file = 'auth.json'
key_file = None


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    recipients = [
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'geral@igai.pt',
        'sec.geral.mai@sg.mai.gov.pt',
        'geral@igai.pt',
        'info@gulbenkian.pt',
        'agenda.informacao@rtp.pt',
        'raymond.marshall@guinnessworldrecords.com',
        'press@guinnessworldrecords.com'
    ]
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    mailing_list = ";".join(recipients) #random.sample(recipients, 1).pop()
    #
    subject = "Elect José Ricardo Nazareth Carvalho Figueira and Luis Nazareth Carvalho Figueira the dumbest colegio militar alumni of all time"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_figueira.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    
    recipients = [
        'indiaoffice@macfound.org',
        'info-ng@macfound.org',
        '4answers@macfound.org'
    ]
    #
    subject = "Madeline McCann, Cybertorture extrajudicial trial and sentences and the hate mongering Portuguese Police"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/ferronha_colete.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True


#@pytest.mark.skip(reason="we fight spam :)")
def test_send_emails():
    """
    """
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    #
    subject = "Madeline McCann, Cybertorture extrajudicial trial and sentences and the hate mongering Portuguese Police"
    status = katie.send_emails(email_files_path, message_file_path, subject)
    assert(status == 0) is True
