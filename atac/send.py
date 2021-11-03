import os
import sys
import smtplib
import ssl
import csv
import json
import markdown
import time
from random import randint
from tqdm import tqdm

from bs4 import BeautifulSoup
from validator_collection import checkers
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import phonenumbers
from phonenumbers import NumberParseException, phonenumberutil
from twilio.rest import Client
from .whatsapp import Client
if os.environ.get('DISPLAY'):
    from pywhatkit import *

import facebook
import tweepy

from .config import Config


class FromRuXiaWithLove:


    def __init__(self):
        self.config = Config()
        self.email = self.config.data['email']
        self.phone = self.config.data['phone']
        self.social = self.config.data['social']


    def compose_email(self, mailing_list, path_message, subject):
        content_index = self.email['active_content']
        auth_index = self.email['active_auth']
        content = self.email['content'][content_index]
        auth = self.email['auth'][auth_index]
        #
        message = MIMEMultipart("alternative")
        if subject:
            message["Subject"] = subject
        elif path_message:
            message["Subject"] = ""
        else:
            message["Subject"] = content['subject']
        message["From"] = auth['sender']
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        text = ""
        html = ""
        # convert markdown to html
        if path_message:
            message_file = path_message
        else:
            md = 'assets/mail_content/' + content['markdown']
            mesage_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', md))
        #
        with open(message_file, 'r') as f:
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


    def update_config(self):
        # reload config
        self.config.load_config()
        # get active auth
        content_ndx = self.email['active_content']
        auth_ndx = self.email['active_auth']
        auth = self.email['auth'][auth_ndx]
        # set sctive to next and save config
        if self.email['rotate_content']:
            self.email['active_content'] = (1 + content_ndx) % len(self.email['content'])
        # set active auth to next and save config
        if self.email['rotate_auth']:
            self.email['active_auth'] = (1 + auth_ndx) % len(self.email['auth'])
        self.config.save_config()


    def get_ml_files(self, path):
        ml_files = None
        if os.path.isdir(path):
            ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        elif os.path.isfile(path):
            ml_files = [path]
        return ml_files


    def get_numbers(self, path):
        # Open the people CSV and get all the numbers out of it
        numbers = []
        ml_files = self.get_ml_files(path)
        #
        for ml in ml_files:
            if os.path.isdir(path):
                cf = path + ml
            elif os.path.isfile(path):
                cf = ml
            print(cf)
            with open(cf) as file:
                lines = [line for line in file]
                with tqdm(total=len(lines)) as progress:
                    for ndx, phone in csv.reader(lines):
                        print(phone)
                        try:
                            z = phonenumbers.parse(phone)
                            valid_number = phonenumbers.is_valid_number(z)
                            if valid_number:
                                line_type = phonenumberutil.number_type(z)
                                if line_type == 1:
                                    numbers.append(phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164))
                        except NumberParseException as e:
                            print(str(e))
        return numbers


    def get_msg(self, message_file):
        # Now put your SMS in a file called message.txt, and it will be read from there.
        with open(message_file, encoding="utf8") as content_file:
            msg = content_file.read()
        # Check we read a message OK
        if len(msg.strip()) == 0:
            print("SMS message not specified- please make a {}' file containing it. \r\nExiting!".format(message_file))
            sys.exit(1)
        else:
            print("> SMS message to send: \n\n{}".format(msg))
        return msg


    def send_email(self, mailing_list, message):
        content_index = self.email['active_content']
        auth_index = self.email['active_auth']
        content = self.email['content'][content_index]
        auth = self.email['auth'][auth_index]
        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(auth['server'], auth['port'], context=context) as server:
                server.set_debuglevel(1)
                server.login(auth['user'], auth['password'])
                server.sendmail(auth['sender'], mailing_list, message.as_string())
        except Exception as err:
            print(f'\x1b[6;37;41m error occurred: {err}\x1b[0m')
        finally:
            print("\x1b[6;37;42m Sent \x1b[0m")
            
            
    def store_emails_in_buckets(self, lines, ml_emails):
        ml_counter = 0
        num_buckets = len(ml_emails)
        with tqdm(total=len(lines)) as progress:
            for ndx, receiver_email in csv.reader(lines):
                if checkers.is_email(receiver_email):
                    current_bucket = ml_counter % num_buckets      
                    ml_emails[current_bucket].append(receiver_email)
                    ml_counter += 1
                    progress.update(1)


    def send_emails_in_buckets(self, ml_emails, path_message, subject):
        with tqdm(total=len(ml_emails)) as progress:
            for ml_batch in ml_emails:
                mailing_list = '; '.join(ml_batch)
                message = self.compose_email(mailing_list, path_message, subject)
                self.send_email(mailing_list, message)
                time.sleep(5)
                progress.update(1)


    def send_emails(self, path_emails, path_message, subject):
        print(path_emails)
        status = 0
        ml_files = self.get_ml_files(path_emails)
        for ml in ml_files:
            cf = path_emails + ml
            print(cf)
            with open(cf) as file:
                lines = [line for line in file]
                num_emails_per_bucket = 1
                num_buckets = len(lines) // num_emails_per_bucket
                ml_emails = [[] for i in range(num_buckets)]
                self.store_emails_in_buckets(lines, ml_emails)
                self.send_emails_in_buckets(ml_emails, path_message, subject)
        self.update_config()
        return status


    def calculate_twilio_cost(self, msg, phone_numbers, msg_type):
        SMS_LENGTH = 160                 # Max length of one SMS message
        WHATSAPP_MSG_COST = 0.005        # Cost per message
        SMS_MSG_COST = 0.005        # Cost per message
        # How many segments is this message going to use?
        num_segments = 0
        if msg_type == "whatsapp":
            num_segments = 1
        else:
            num_segments = int(len(sms.encode('utf-8')) / SMS_LENGTH) +1
        # Calculate how much it's going to cost:
        num_messages = len(phone_numbers)
        cost = 0
        if msg_type == "whatsapp":
            cost = WHATSAPP_MSG_COST * num_messages
        else:
            cost = SMS_MSG_COST * num_segments * num_messages
            print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(num_messages, num_segments, cost))


    def send_twilio(self, path, message_file, msg_type):
        msg = self.get_msg(message_file)
        phone_numbers = self.get_numbers(path)
        # Check you really want to send them
        self.calculate_twilio_cost(msg, phone_numbers, msg_type)
        confirm = input("Send these messages? [Y/n] ")
        if confirm[0].lower() == 'y':
            # Set up Twilio client
            account_sid = self.phone['twilio']['SID']
            auth_token = self.phone['twilio']['TOKEN']
            from_num = self.phone['twilio']['PHONE'] # 'From' number in Twilio
            client = Client(account_sid, auth_token)
            # Send the messages
            for num in phone_numbers:
                try:
                    # Send the sms text to the number from the CSV file:
                    if msg_type == "whatsapp":
                        num = "whatsapp:"+num
                        from_num = "whatsapp:"+from_num
                    print("Sending to " + num)
                    message = client.messages.create(to=num, from_=from_num, body=msg)
                except Exception as e:
                    print(str(e))
                finally:
                    time.sleep(1)
        #
        print("Exiting!")


    def send_yowsup(self, path, message_file):
        msg = self.get_msg(message_file)
        phone_numbers = self.get_numbers(path)
        # Check you really want to send them
        confirm = input("Send these messages? [Y/n] ")
        if confirm[0].lower() == 'y':
            user = self.phone['yowsup']['user']
            password = self.phone['yowsup']['password']
            client = Client(login=user, password=password)
            # Send the messages
            for num in phone_numbers:
                try:
                    print("Sending to " + num)
                    client.send_message(num, msg)
                except Exception as e:
                    print(str(e))
                finally:
                    time.sleep(1)
        #
        print("Exiting!")


    if os.environ.get('DISPLAY'):
        def send_pywhatkit(self, path, message_file):
            msg = self.get_msg(message_file)
            phone_numbers = self.get_numbers(path)
            # Check you really want to send them
            confirm = input("Send these messages? [Y/n] ")
            if confirm[0].lower() == 'y':
                # Send the messages
                for num in phone_numbers:
                    try:
                        print("Sending to " + num)
                        pywhatkit.sendwhatmsg_instantly(num, msg, 15, True, 5)
                    except Exception as e:
                        print(str(e))
                    finally:
                        time.sleep(1)
            #
            print("Exiting!")


    def send_facebook(self):
        status = 0
        msg = "Hello, world!"
        graph = facebook.GraphAPI(self.social['facebook']['access_token'])
        link = 'https://www.jcchouinard.com/'
        groups = ['744128789503859']
        for group in groups:
            graph.put_object(group, 'feed', message=msg, link=link)
            print(graph.get_connections(group, 'feed'))
        return status


    def send_twitter(self):
        status = 0
        CONSUMER_KEY = self.social['twitter']['consumer_key']
        CONSUMER_SECRET = self.social['twitter']['consumer_secret']
        ACCESS_TOKEN = self.social['twitter']['access_token']
        ACCESS_TOKEN_SECRET = self.social['twitter']['access_token_secret']
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        handles = sys.argv[1]
        f = open(handles, "r")
        h = f.readlines()
        f.close()
        for i in h:
            i = i.rstrip()
            m = i + " " + sys.argv[2]
            s = api.update_status(m)
            nap = randint(1, 60)
            time.sleep(nap)
        return status
