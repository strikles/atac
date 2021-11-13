import os
import sys
import json
import markdown
import markovify

from email import charset
from email.encoders import encode_base64
from email.header import Header
from email.message import Message
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

    @staticmethod
    def fix_mixed_encoding(s):
        output = ''
        ii = 0
        for c in s:
            if ii <= len(s)-1:
                if s[ii] == '\\' and s[ii+1] == 'x':
                    b = s[ii:ii+4].encode('ascii').decode('unicode-escape')
                    output = output+b
                    ii += 3
                else:
                    output = output+s[ii]
            ii += 1
        return output

    def compose_email(self, sender_email, mailing_list, message_file_path, subject):
        #
        message = Message()
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        #
        message["Subject"] = Header(self.fix_mixed_encoding(subject), 'utf-8')
        message["From"] = self.fix_mixed_encoding(sender_email).encode('utf-8')
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        text = None
        html = None
        # Turn these into plain/html MIMEText objects
        part1 = MIMENonMultipart("text", "plain", charset=cs)
        part2 = MIMENonMultipart("text", "html", charset=cs)
        # convert markdown to html
        with open(message_file_path, encoding="utf-8") as message_file:
            text = self.fix_mixed_encoding(message_file.read()).encode('utf-8')
            html = markdown.markdown(text).encode('utf-8')
        part1.set_payload(text, charset=cs)
        part2.set_payload(html, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        body.attach(part1)
        body.attach(part2)
        #
        message.attach(body)
        print(message.as_string())
        #
        return message

    def get_message(self, message_file_path):
        #
        if not os.path.isfile(message_file_path):
            print("invalid message file path!")
            sys.exit(1)
        msg = None
        # Now put your SMS in a file called message.txt, and it will be read from there.
        with open(message_file_path, encoding="utf-8") as content_file:
            msg = content_file.read()
        # Check we read a message OK
        if len(msg.strip()) == 0:
            print("message file is empty!")
            sys.exit(1)
        else:
            print("> message to send: \n\n{}".format(msg))
        #
        return msg
