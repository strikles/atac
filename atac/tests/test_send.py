import os
import sys
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None


def test_send_email():
    """
    """
    mailing_list = "perceptionchange@un.org"
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    auth, _ = katie.get_email_config()
    message_content = katie.get_file_content(os.getcwd() + "/atac/tests/test_message.md", "message")
    message = katie.compose_email(auth['sender'], mailing_list, message_content, subject)
    katie.send_email(mailing_list, message)


def test_send_emails():
    """
    """
    email_files_path = os.getcwd() + "/atac/tests/test_emails.csv"
    message_file_path = os.getcwd() + "/atac/tests/test_message.md"
    subject = "Cybertorture extrajudicial sentences and the Portuguese Police"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    katie.send_emails(email_files_path, message_file_path, subject)
