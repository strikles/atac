import os
import sys
import json
import markdown
import markovify

from email import charset
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from email.mime.text import MIMEText
import mimetypes


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
        email = MIMEMultipart('mixed')
        #
        #cs_ = charset.Charset('utf-8')
        #cs_.header_encoding = charset.QP
        #cs_.body_encoding = charset.QP
        #email.set_charset(cs_)
        #
        email["Subject"] = subject
        email["From"] = sender_email
        email["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        message = MIMEMultipart("alternative")
        text = None
        html = None
        # Turn these into plain/html MIMEText objects
        part1 = MIMENonMultipart("text", "plain")
        part1.add_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        part2 = MIMENonMultipart("text", "html")
        part2.add_header('Content-Transfer-Encoding', 'quoted-printable')
        # convert markdown to html
        with open(message_file_path) as message_file:
            text = message_file.read()
            html = markdown.markdown(text)
        part1.set_payload(text)
        part2.set_payload(html)
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        #
        email.attach(message)
        print(email.as_string())
        #
        return email

    def get_message(self, message_file_path):
        #
        if not os.path.isfile(message_file_path):
            print("invalid message file path!")
            sys.exit(1)
        msg = None
        # Now put your SMS in a file called message.txt, and it will be read from there.
        with open(message_file_path, encoding="utf8") as content_file:
            msg = content_file.read()
        # Check we read a message OK
        if len(msg.strip()) == 0:
            print("message file is empty!")
            sys.exit(1)
        else:
            print("> message to send: \n\n{}".format(msg))
        #
        return msg
