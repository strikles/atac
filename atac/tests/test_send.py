import os
import random
import sys
import pytest
import atac


encrypted_config = True
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
        'sec.geral.mai@sg.mai.gov.pt'
    ]
    #
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    mailing_list = random.sample(recipients, 1).pop()
    #
    subject = "Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_pt.md", "message"))
    mailing_list = random.sample(recipients, 1).pop()
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    status = katie.send_email(mailing_list, message)
    assert(status == 0) is True
    #
    subject = "This is a request for emergency humanitarian help to address the threat the Portuguese police represents to the families of their cybertorture victims"
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_figueira.md", "message"))
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
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    status = katie.send_emails(email_files_path, message_file_path, subject)
    assert(status == 0) is True
    #
    message_file_path = os.getcwd() + "/atac/tests/test_message_figueira.md"
    subject = "This is a request for emergency humanitarian help to address the threat the Portuguese police represents to the families of their cybertorture victims"
    status = katie.send_emails(email_files_path, message_file_path, subject)
    assert(status == 0) is True