import os
import sys
import json
import markdown
import markovify

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AllTimeHigh(object):

    def __init__(self, a, b, c):
        pass

    @staticmethod
    def gen_content(content):
        status = 0
        # Get raw text as string.
        with open(content) as f:
            text = f.read()
        # Build the model.
        text_model = markovify.Text(text, state_size=3)
        # Print five randomly-generated sentences
        for i in range(5):
            print(text_model.make_sentence(tries=100))
        # Print three randomly-generated sentences of no more than 280 characters
        for i in range(3):
            print(text_model.make_short_sentence(280))
        return status

    def compose_email(self, sender_email, mailing_list, message_file_path, subject):
        #
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        #
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        text = ""
        html = ""
        # convert markdown to html
        with open(message_file_path, 'r') as message_file:
            ptext = message_file.read()
            html = markdown.markdown(ptext)
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        #
        return message
