import os
import sys
import smtplib
import ssl
import csv
import json
import markdown
import time
from bs4 import BeautifulSoup
from validator_collection import checkers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint
from tqdm import tqdm

class FromRuXiaWithLove:

    def __init__(self):
        self.config = {}
        with open('auth.json') as json_file:
            self.config = json.load(json_file)
            
    def compose_email(self, content, auth, mailing_list):
       # compose email
        message = MIMEMultipart("alternative")
        message["Subject"] = content['subject']
        message["From"] = auth['sender']
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        text = ""
        html = ""
        # convert markdown to html
        md = 'assets/mail_content/' + content['markdown']
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', md)), 'r') as f:
            ptext = f.read()
            html = markdown.markdown(ptext)
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        return message
        
    def send_email(self, path):
        
        print(path)
        status = 0
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        batch_size = min(1, 2000)
        
        # reload config
        with open('auth.json') as json_file:
            self.config = json.load(json_file)
        # get active auth
        email_cfg = self.config['send']['email']
        auth_ndx = email_cfg['active_auth']
        auth = email_cfg['auth'][auth_ndx]
        # get active content
        content_ndx = email_cfg['active_content']
        content = email_cfg['content'][content_ndx]
        
        # set sctive to next and save config
        if email_cfg['rotate_content']:
            email_cfg['active_content'] = (1 + content_ndx) % len(email_cfg['content'])
        # set active auth to next and save config
        if email_cfg['rotate_auth']:
            email_cfg['active_auth'] = (1 + auth_ndx) % len(email_cfg['auth'])
        with open('auth.json', 'w') as fp:
            self.config['send']['email'] = email_cfg
            json.dump(self.config, fp, indent=4)
        
        for ml in ml_files:
            cf = path + ml
            print(cf)
            
            with open(cf) as file:
                lines = [line for line in file]
                num_batches = len(lines) // batch_size
                ml_emails = [[] for i in range(num_batches)]
                ml_counter = 0

                with tqdm(total=len(lines)) as progress:
                    for ndx, receiver_email in csv.reader(lines):
                        if checkers.is_email(receiver_email):           
                            ml_emails[ml_counter // num_batches].append(receiver_email)
                            ml_counter += 1
                        progress.update(1)

                with tqdm(total=len(ml_emails)) as progress2:
                    for ml_batch in ml_emails:
                        mailing_list = '; '.join(ml_batch)
                        message = self.compose_email(content, auth, mailing_list)
                        
                        # Create secure connection with server and send email
                        try:
                            context = ssl.create_default_context()
                            with smtplib.SMTP_SSL(auth['server'], auth['port'], context=context) as server:
                                server.login(auth['user'], auth['password'])
                                server.sendmail(auth['sender'], mailing_list, message.as_string())
                        except Exception as err:
                            print(f'\x1b[6;37;41m error occurred: {err}\x1b[0m')
                        finally:
                            print("\x1b[6;37;42m Sent \x1b[0m")

                        time.sleep(5)
                        progress2.update(1)
                
        return status

    def send_whatsapp(self, path):
        status = 0
        # Your Account Sid and Auth Token from twilio.com/console
        # and set the environment variables. See http://twil.io/secure
        account_sid = self.config['twilio']['ACCOUNT_SID']
        auth_token = self.config['twilio']['AUTH_TOKEN']
        # get mailing list csv files
        phone_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        # send mesg
        for phone in phone_files:
            cp = path + phone
            print(cp)
            with open(cp) as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for num, phone_number in reader:
                    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
                    client = Client(account_sid, auth_token)
                    # this is the Twilio sandbox testing number
                    from_whatsapp_number = 'whatsapp:+14155238886'
                    # replace this number with your own WhatsApp Messaging number
                    to_whatsapp_number = 'whatsapp:' + phone_number
                    ndx = 0
                    content = self.config['email']['content'][ndx]
                    # convert markdown to html
                    md = '/assets/mail_content/' + content['markdown']
                    with open(os.path.dirname(os.path.abspath(__file__)) + md, 'r') as f:
                        ptext = f.read()
                        html = markdown.markdown(ptext)
                        soup = BeautifulSoup(html, features='html.parser')
                        message = client.messages \
                            .create(
                            body=soup.get_text(),
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number
                        )
                        print(message.sid)
        return status
