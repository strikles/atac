import os
import sys
import atac


encrypted_config = True
config_file = 'auth.json'
key_file = None

def test_send_email():
    """
    """
    sender_email = ""
    mailing_list = ["civilsociety@ohchr.org"]
    message_content = "This is a test atac email"
    subject = "test atac email"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    message = katie.compose_email(sender_email, mailing_list, message_content, subject)
    katie.send_email(mailing_list, message)

def test_send_emails():
    """
    """
    email_files_path = "test_emails.csv"
    message_file_path = "test_message.md"
    subject = "test atac email"
    katie = atac.FromRuXiaWithLove(encrypted_config, config_file, key_file)
    katie.send_emails(email_files_path, message_file_path, subject)