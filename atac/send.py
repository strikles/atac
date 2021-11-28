from .compose import AllTimeHigh
from .art import *
import csv
from envelope import Envelope
import frontmatter
import markdown2
import os
import smtplib
import socket
import ssl
import sys
import textwrap
import time
from tqdm import tqdm

import phonenumbers
from phonenumbers import NumberParseException, phonenumberutil

if os.environ.get('DISPLAY'):
    from pywhatkit import *

from twilio.rest import Client as TwilioClient

from validate_email import validate_email
import validators


class FromRuXiaWithLove(AllTimeHigh):
    """
    A class used to represent a Configuration object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG

    Methods
    -------
    generate_key()
        Generates a new encryption key from a password + salt
    """

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        """
        Class init

        Parameters
        ----------
        encrypted_config : bool
            use an encrypted configuration file
        config_file_path : str
            path to the configuration file
        key_file_path : str
            path to encryption key file
        """
        super().__init__(encrypted_config, config_file_path, key_file_path)
        self.email = self.data['email']
        self.phone = self.data['phone']
        self.social = self.data['social']

    @staticmethod
    def get_file_content(file_path, file_type='contact'):
        """
        Get file content

        Parameters
        ----------
        file_path : str
            The sound the animal makes
        file_type : int, optional
            The number of legs the animal (default is 4)
        """
        if not os.path.isfile(file_path):
            print("invalid file path!")
            sys.exit(1)
        lines = None
        # Now put your SMS in a file called message.txt, and it will be read from there.
        try:
            with open(file_path, encoding="utf-8") as content_file:
                lines = [line.rstrip() for line in content_file]
                if file_type == 'message':
                    for i in range(len(lines)):
                        lines[i] = textwrap.wrap(text=lines[i], width=70, break_long_words=False)
                    lines = [item for sublist in lines for item in sublist]
                # print('\n>>> '.join(map(str, lines)))
        except OSError as e:
            print('{} file error {}'.format(file_path, e.errno))
        finally:
            content_file.close()
        #
        # print("> file content: \n\n{}".format('\n'.join(lines)))
        #
        return lines

    def get_email_config(self):
        """
        Get email config

        """
        content_index = self.email['active_content']
        auth_index = self.email['active_auth']
        content = self.email['content'][content_index]
        auth = self.email['auth'][auth_index]
        #
        return auth, content

    def update_email_config(self):
        """
        Update email config

        """
        auth, content = self.get_email_config()
        # set sctive to next and save config
        if self.email['rotate_content']:
            self.email['active_content'] = (1 + self.email['active_content']) % len(content)
        # set active auth to next and save config
        if self.email['rotate_auth']:
            self.email['active_auth'] = (1 + self.email['active_auth']) % len(auth)
        #
        self.save_config(self.config_file_path, self.encrypted_config)

    @staticmethod
    def get_contact_files(contact_files_path):
        """
        Get contact files

        Parameters
        ----------
        contact_files_path : str
            The path to the contacts CSV
        """
        contact_files = []
        #
        if os.path.isdir(contact_files_path):
            contact_file_names = list(filter(lambda c: c.endswith('.csv'), os.listdir(contact_files_path)))
            for file_name in contact_file_names:
                file_full_path = os.path.join(contact_files_path, file_name)
                print(file_full_path)
                if os.path.isfile(file_full_path):
                    contact_files.append(file_full_path)
        elif os.path.isfile(contact_files_path):
            contact_files = [contact_files_path]
        else:
            print("Invalid contact file path!")
            sys.exit(1)
        #
        return contact_files

    def get_phone_numbers(self, contact_files_path):
        """
        Open the people CSV and get all the numbers out of it

        Parameters
        ----------
        contact_files_path : str
            The path to the phone numbers CSV
        """
        phone_numbers = []
        contact_files = self.get_contact_files(contact_files_path)
        #
        for file_path in contact_files:
            contact_file = self.get_file_contents(file_path)
            for _, phone in csv.reader(contact_file):
                print(phone)
                try:
                    z = phonenumbers.parse(phone)
                except NumberParseException as e:
                    print(str(e))
                    continue
                valid_number = phonenumbers.is_valid_number(z)
                if valid_number:
                    line_type = phonenumberutil.number_type(z)
                    if line_type == phonenumberutil.PhoneNumberType.MOBILE:
                        phone_number_e164 = phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.E164)
                        phone_numbers.append(phone_number_e164)
        #
        return phone_numbers

    def send_email(self, mailing_list, message):
        """
        Send email

        Parameters
        ----------
        mailing_list : list
            The emails list
        message : MIMEMultipart
            The email messsage to send
        """
        auth, _ = self.get_email_config()
        # Create secure connection with server and send email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(auth['server'], auth['port'], context=context) as server:
                #server.set_debuglevel(2)
                server.login(auth['user'], auth['password'])
                """
                server.ehlo() # Can be omitted
                server.starttls(context=context) # Secure the connection
                server.ehlo() # Can be omitted
                """
                error_status = server.sendmail(auth['sender'], mailing_list, message.as_string())
                print(error_status)
                print("\x1b[6;37;42m Sent \x1b[0m")
                server.quit()
        except Exception as err:
            print(f'\x1b[6;37;41m {type(err)} error occurred: {err}\x1b[0m')

    def find_gpg_keyid(self, recipient):
        """
        We need the keyid to encrypt the message to the recipient.
        Let's walk through all keys in the keyring and find the
        appropriate one

        Parameters
        ----------
        recipient : str
            The email recipient
        """
        keys = self.gpg.list_keys()
        for key in keys:
            for uid in key['uids']:
                if recipient in uid:
                    return key['keyid']
        #
        return None

    def store_emails_in_buckets(self, lines):
        """
        Store emails in buckets

        Parameters
        ----------
        lines : list
            The contacts list
        """
        encrypted_emails = []
        unencrypted_emails = []
        auth, content = self.get_email_config()
        #
        with tqdm(total=len(lines)) as filter_progress:
            for _, receiver_email in csv.reader(lines):
                #
                is_valid_email = validators.email(receiver_email)
                """
                validate_email(
                    email_address=receiver_email,
                    check_format=True,
                    check_blacklist=False,
                    check_dns=False,
                    dns_timeout=10,
                    check_smtp=False,
                    smtp_timeout=10,
                    smtp_helo_host=auth['server'],
                    smtp_from_address=auth['sender'],
                    smtp_skip_tls=False,
                    smtp_tls_context=None,
                    smtp_debug=True)
                """
                #
                if is_valid_email:
                    gpg_key_id = self.find_gpg_keyid(receiver_email)
                    if gpg_key_id:
                        encrypted_emails.append([receiver_email, gpg_key_id])
                    else:
                        unencrypted_emails.append(receiver_email)
                #
                filter_progress.update(1)
        #
        counter = 0
        num_emails_per_bucket = 500
        num_buckets = 1
        if len(unencrypted_emails) > num_emails_per_bucket:
            num_buckets = len(unencrypted_emails) // num_emails_per_bucket
        batch_emails = [[] for i in range(num_buckets)]
        #
        with tqdm(total=len(unencrypted_emails)) as batch_progress:
            for unencrypted_email in unencrypted_emails:
                current_bucket = counter % num_buckets
                batch_emails[current_bucket].append(unencrypted_email)
                counter += 1
                #
                batch_progress.update(1)
        #
        return batch_emails, encrypted_emails

    def send_emails_in_buckets_envelope(self, unencrypted_email_batches, encrypted_emails, message_file_path, subject):
        """
        Send emails in buckets using envelope

        Parameters
        ----------
        unencrypted_email_batches : list
            The name of the animal
        encrypted_emails : list
            The sound the animal makes
        message_file_path : str
            The number of legs the animal (default is 4)
        subject : str
            The email subject
        """
        auth, _ = self.get_email_config()
        message_content = []
        with open(message_file_path, encoding="utf-8") as content_file:
            message_content = content_file.readlines()
            print(message_content)
        message = ""
        for line in message_content:
            message += markdown2.markdown(line)
        print(message)
        #
        with tqdm(total=len(unencrypted_email_batches)) as progress:
            for batch in unencrypted_email_batches:
                mailing_list = '; '.join(batch)
                generate_art_samila()
                time.sleep(10)
                e = (Envelope("<img src='cid:art.png' />")
                    .subject(subject)
                    .message(message)
                    .from_(auth['sender'])
                    .to(mailing_list)
                    .attach(path="art.png", inline=True)
                    .smtp(auth['server'], auth['port'], auth['user'], auth['password'], "starttls")
                    #.check(check_mx=True, check_smtp=True)
                    .send(send=True))
                #
                print(type(e), e.as_message())
                #
                progress.update(1)
        #
        with tqdm(total=len(encrypted_emails)) as encrypted_progress:
            for email_recipient, gpg_key_id in encrypted_emails:
                generate_art_samila()
                time.sleep(10)
                e = (Envelope("<img src='cid:art.png' />")
                    .subject(subject)
                    .message(message)
                    .from_(auth['sender'])
                    .to(email_recipient)
                    .encryption()
                    .attach(path="art.png", inline=True)
                    .smtp(auth['server'], auth['port'], auth['user'], auth['password'], "starttls")
                    #.check(check_mx=True, check_smtp=True)
                    .send(send=True))
                #
                print(type(e), e.as_message())
                #
                encrypted_progress.update(1)

    def send_emails_in_buckets(self, unencrypted_email_batches, encrypted_emails, message_file_path, subject):
        """
        Send emails in buckets

        Parameters
        ----------
        unencrypted_email_batches : list
            The name of the animal
        encrypted_emails : list
            The sound the animal makes
        message_file_path : str
            The number of legs the animal (default is 4)
        subject : str
            The email subject
        """
        print(subject)
        auth, _ = self.get_email_config()
        message_content = []
        with open(message_file_path, encoding="utf-8") as content_file:
            message_content = content_file.readlines()
        message = ""
        for line in message_content:
            message += markdown2.markdown(line)
        #
        with tqdm(total=len(unencrypted_email_batches)) as progress:
            for batch in unencrypted_email_batches:
                mailing_list = '; '.join(batch)
                mime_message = self.compose_email(auth['sender'],
                                                mailing_list,
                                                message,
                                                subject)
                #
                self.send_email(mailing_list, mime_message)
                #
                time.sleep(5)
                progress.update(1)
        #
        with tqdm(total=len(encrypted_emails)) as encrypted_progress:
            for email_recipient, gpg_key_id in encrypted_emails:
                encrypted_mime_message = self.compose_encrypted_email(auth['sender'],
                                                                    email_recipient,
                                                                    gpg_key_id,
                                                                    message,
                                                                    subject)
                #
                self.send_email(email_recipient, encrypted_mime_message)
                #
                time.sleep(1)
                encrypted_progress.update(1)

    def send_emails(self, email_files_path, message_file_path, subject):
        """
        Send Emails

        Parameters
        ----------
        unencrypted_email_batches : list
            The name of the animal
        email_file_path : str
            The sound the animal makes
        message_file_path : str
            The number of legs the animal (default is 4)
        subject : str
            The email subject
        """
        status = 0
        #
        if not os.path.isfile(message_file_path):
            print("Invalid message file path!")
            sys.exit(1)
        #
        print(email_files_path)
        email_files = self.get_contact_files(email_files_path)
        for email_file_path in email_files:
            contact_file = self.get_file_content(email_file_path)
            unencrypted_emails, encrypted_emails = self.store_emails_in_buckets(contact_file)
            self.send_emails_in_buckets(unencrypted_emails, encrypted_emails, message_file_path, subject)
        #
        self.update_email_config()
        #
        return status

    def send_emails_envelope(self, email_files_path, message_file_path, subject):
        """
        Send Emails

        Parameters
        ----------
        unencrypted_email_batches : list
            The name of the animal
        email_file_path : str
            The sound the animal makes
        message_file_path : str
            The number of legs the animal (default is 4)
        subject : str
            The email subject
        """
        status = 0
        #
        if not os.path.isfile(message_file_path):
            print("Invalid message file path!")
            sys.exit(1)
        #
        print(email_files_path)
        email_files = self.get_contact_files(email_files_path)
        for email_file_path in email_files:
            contact_file = self.get_file_content(email_file_path)
            unencrypted_emails, encrypted_emails = self.store_emails_in_buckets(contact_file)
            self.send_emails_in_buckets_envelope(unencrypted_emails, encrypted_emails, message_file_path, subject)
        #
        self.update_email_config()
        #
        return status

    @staticmethod
    def calculate_twilio_cost(msg, phone_numbers, msg_type):
        """
        Calculate Twilio cost

        Parameters
        ----------
        msg : str
            The name of the animal
        phone_numbers : list
            The sound the animal makes
        msg_type : str
            The number of legs the animal (default is 4)
        """
        SMS_LENGTH = 160            # Max length of one SMS message
        WHATSAPP_MSG_COST = 0.005   # Cost per message
        SMS_MSG_COST = 0.005        # Cost per message
        # How many segments is this message going to use?
        num_segments = 0
        if msg_type == "whatsapp":
            num_segments = 1
        else:
            num_segments = int(len(msg.encode('utf-8')) / SMS_LENGTH) + 1
        # Calculate how much it's going to cost:
        num_messages = len(phone_numbers)
        cost = 0
        if msg_type == "whatsapp":
            cost = WHATSAPP_MSG_COST * num_messages
        else:
            cost = SMS_MSG_COST * num_segments * num_messages
            print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(num_messages, num_segments, cost))

    def send_twilio(self, contacts_file_path, message_file_path, msg_type):
        """
        Send Twilio message

        Parameters
        ----------
        contacts_file_path : str
            The name of the animal
        message_file_path : str
            The sound the animal makes
        msg_type : str
            The number of legs the animal (default is 4)
        """
        msg = u'\n'.join(self.get_file_content(message_file_path, 'message'))
        phone_numbers = self.get_phone_numbers(contacts_file_path)
        # Check you really want to send them
        self.calculate_twilio_cost(msg, phone_numbers, msg_type)
        #
        confirm = input("Send these messages? [Y/n] ")
        if confirm[0].lower() != 'y':
            sys.exit(1)
        # Set up Twilio client
        account_sid = self.phone['twilio']['SID']
        auth_token = self.phone['twilio']['TOKEN']
        from_num = self.phone['twilio']['PHONE']
        client = TwilioClient(account_sid, auth_token)
        # Send the messages
        for num in phone_numbers:
            try:
                # Send the sms text to the number from the CSV file:
                if msg_type == "whatsapp":
                    num = "whatsapp:"+num
                    from_num = "whatsapp:"+from_num
                print("Sending to " + num)
                message = client.messages.create(to=num, from_=from_num, body=msg)
                print(message.sid)
            except Exception as e:
                print(str(e))
            finally:
                time.sleep(1)
        #
        print("Exiting!")

    """
    def send_yowsup(self, contacts_file_path, message_file_path):
        #
        msg = self.get_message(message_file_path)
        phone_numbers = self.get_phone_numbers(contacts_file_path)
        # Check you really want to send them
        confirm = input("Send these messages? [Y/n] ")
        if confirm[0].lower() == 'y':
            user = self.phone['yowsup']['user']
            password = self.phone['yowsup']['password']
            client = YowsupClient(login=user, password=password)
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
    """

    if os.environ.get('DISPLAY'):
        def send_pywhatkit(self, contacts_file_path, message_file_path):
            """
            Send Pywhatkit message

            Parameters
            ----------
            contacts_file_path : str
                The path to the phone numbers CSV
            message_file_path : str
                The path to the message file
            """
            msg = u'\n'.join(self.get_file_content(message_file_path, 'message'))
            phone_numbers = self.get_phone_numbers(contacts_file_path)
            # Check you really want to send them
            confirm = input("Send these messages? [Y/n] ")
            if confirm[0].lower() != 'y':
                sys.exit(1)
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

    def send_signal(self, contacts_file_path, message_file_path):
        """
        Send Signal message

        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        """

        r"""
        msg = u'\n'.join(self.get_file_content(message_file_path))
        phone_numbers = self.get_phone_numbers(contacts_file_path)
        # Check you really want to send them
        confirm = input("Send these messages? [Y/n] ")
        if confirm[0].lower() != 'y':
            sys.exit(1)
        # create new signal-cli object (will automatically start signal-cli in the background)
        sig = signalcli.Signalcli(debug=True, user_name="+46123456789")
        # Send the messages
        for num in phone_numbers:
            try:
                print("Sending to " + num)
                recipient_identity = num
                sig.send_message(recipient_identity, msg, "direct", [])
            except Exception as e:
                print(str(e))
            finally:
                time.sleep(1)
        #
        print("Exiting!")
        """

    def send_facebook(self, message_file_path):
        """
        Send Facebook

        Parameters
        ----------
        name : str
            The name of the animal
        """

        """
        status = 0
        msg = "Hello, world!"
        graph = facebook.GraphAPI(self.social['facebook']['access_token'])
        link = 'https://www.jcchouinard.com/'
        groups = ['744128789503859']
        for group in groups:
            graph.put_object(group, 'feed', message=msg, link=link)
            print(graph.get_connections(group, 'feed'))
        #
        return status
        """

    def send_twitter(self, message_file_path):
        """
        Send Twitter

        Parameters
        ----------
        name : str
            The name of the animal
        """

        """
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
        #
        return status
        """


class IRC:

    irc = socket.socket()

    def __init__(self):
        # Define the socket
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, channel, msg):
        # Transfer data
        self.irc.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))

    def connect(self, server, port, channel, botnick, botpass, botnickpass):
        # Connect to the server
        print("Connecting to: " + server)
        self.irc.connect((server, port))

        # Perform user authentication
        self.irc.send(bytes("USER " + botnick + " " + botnick +" " + botnick + " :python\n", "UTF-8"))
        self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
        self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(5)

        # join the channel
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def get_response(self):
        time.sleep(1)
        # Get the response
        resp = self.irc.recv(2040).decode("UTF-8")

        if resp.find('PING') != -1:
            self.irc.send(bytes('PONG ' + resp.split().decode("UTF-8") [1] + '\r\n', "UTF-8"))

            return resp

    def run(self):
        ## IRC Config
        server = "10.x.x.10" # Provide a valid server IP/Hostname
        port = 6697
        channel = "#python"
        botnick = "techbeamers"
        botnickpass = "guido"
        botpass = "<%= @guido_password %>"
        #
        irc = IRC()
        irc.connect(server, port, channel, botnick, botpass, botnickpass)
        #
        while True:
            text = irc.get_response()
            print(text)

            if "PRIVMSG" in text and channel in text and "hello" in text:
                irc.send(channel, "Hello!")

"""
RPL_NAMREPLY   = '353'
RPL_ENDOFNAMES = '366'

irc = {
    'host':          'chat.freenode.net',
    'port':          6667,
    'channel':       '#raspiuserguide',
    'namesinterval': 5
}

user = {
    'nick':       'botnick',
    'username':   'botuser',
    'hostname':   'localhost',
    'servername': 'localhost',
    'realname':   'Raspberry Pi Names Bot'
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting to {host}:{port}...'.format(**irc))
try:
    s.connect((irc['host'], irc['port']))
except socket.error:
    print('Error connecting to IRC server {host}:{port}'.format(**irc))
    sys.exit(1)

s.send('NICK {nick}\r\n'.format(**user).encode())
s.send('USER {username} {hostname} {servername} :{realname}\r\n'.format(**user).encode())
s.send('JOIN {channel}\r\n'.format(**irc).encode())
s.send('NAMES {channel}\r\n'.format(**irc).encode())

read_buffer = ''
names = []

while True:
    read_buffer += s.recv(1024).decode()
    lines = read_buffer.split('\r\n')
    read_buffer = lines.pop();
    for line in lines:
        response = line.rstrip().split(' ', 3)
        response_code = response[1]
        if response_code == RPL_NAMREPLY:
            names_list = response[3].split(':')[1]
            names += names_list.split(' ')
        if response_code == RPL_ENDOFNAMES:
            print('\r\nUsers in {channel}:'.format(**irc))
            for name in names:
                print(name)
            names = []
            time.sleep(irc['namesinterval'])
            s.send('NAMES {channel}\r\n'.format(**irc).encode())
"""