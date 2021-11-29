import os
import random
import sys
import pytest
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


# @pytest.mark.skip(reason="we fight spam :)")
def test_send_email():
    """
    """
    recipients = [
        'contacto@psp.pt',
        'geral@prociv.pt',
        'gnr@gnr.pt',
        'mail@ansr.pt',
        'sef@sef.pt',
        'sec.geral.mai@sg.mai.gov.pt'
    ]
    mailing_list = random.sample(recipients, 1).pop()
    subject = "Exoneração imediata de ex-alunos do colégio militar associados a Pedro Miguel De Brito Esteves Grilo"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    message_content = '\n'.join(katie.get_file_content(os.getcwd() + "/atac/tests/test_message_pt.md", "message"))
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    katie.send_email(mailing_list, message)


# @pytest.mark.skip(reason="we fight spam :)")
def test_send_emails():
    """
    """
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    katie.send_emails(email_files_path, message_file_path, subject)
