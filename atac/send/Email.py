from .Send import Send
from ..compose.Compose import Compose
from ..util.Util import trace, get_file_content

import base64
import getpass
import email
import logging
import imaplib
import json
import mistune
import os
import poplib
import random
import re
import smtplib
import ssl
import sys
import time
from tqdm import tqdm
import validators


from envelope import Envelope

# Logging
## For results: open << debug.log >>
LOGGER = logging.getLogger("Riseup_Log")
LOGGER.setLevel(logging.DEBUG)
fh = logging.FileHandler("debug.log")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
LOGGER.addHandler(fh)
# LOGGER.debug('Debug-Message')
# LOGGER.info('Info-Message')
# LOGGER.warning('Warning-message')
# LOGGER.error('Error-Message')

#########################################################################################
#                                         A                                             #
#########################################################################################


class SendEmail(Send):
    """A class used to represent a Configuration object

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

    def __init__(
        self, encrypted_config=True, config_file_path="auth.json", key_file_path=None
    ):
        """Class init

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
        self.email = self.data["email"]

    def get_config(self):
        """Get email config"""
        content_index = int(self.email["active_content"])
        auth_index = int(self.email["active_auth"])
        #
        if auth_index > len(self.email["auth"]):
            print("Invalid active_auth index in your .json config")
            sys.exit(1)
        #
        if content_index > len(self.email["content"]):
            print("Invalid active_content index in your .json config")
            sys.exit(1)
        #
        content = self.email["content"][content_index]
        auth = self.email["auth"][auth_index]
        #
        return auth, content

    def update_config(self):
        """Update email config"""
        auth, content = self.get_config()
        # set sctive to next and save config
        if self.email["rotate_content"]:
            self.email["active_content"] = (1 + self.email["active_content"]) % len(
                content
            )
        # set active auth to next and save config
        if self.email["rotate_auth"]:
            self.email["active_auth"] = (1 + self.email["active_auth"]) % len(auth)
        #
        self.save_config(self.config_file_path, self.encrypted_config)

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
            for uid in key["uids"]:
                if recipient in uid:
                    return key["keyid"]
        #
        return None

    def store_emails_in_buckets(self, lines):
        """Store emails in buckets

        Parameters
        ----------
        lines : list
            The contacts list
        """
        max_emails_per_bucket = 2000
        auth, content = self.get_config()
        recipient_emails = list(
            map(
                lambda z: z.split(",")[1],
                list(
                    filter(
                        trace(
                            lambda x: x.find(",") != -1
                            and validators.email(x.split(",")[1])
                        ),
                        lines,
                    )
                ),
            )
        )
        print("Before shuffling: {}".format(json.dumps(recipient_emails, indent=4)))
        random.seed()
        random.shuffle(recipient_emails)
        print("After shuffling: {}".format(json.dumps(recipient_emails, indent=4)))
        batch_emails = [
            [
                e
                for e in recipient_emails[
                    start_ndx : None
                    if len(recipient_emails[start_ndx:]) < max_emails_per_bucket
                    else start_ndx + max_emails_per_bucket
                ]
            ]
            for start_ndx in range(0, len(recipient_emails), max_emails_per_bucket)
        ]
        print(json.dumps(batch_emails, indent=4))
        return batch_emails

    def send_emails_in_buckets(
        self,
        email_batches,
        message_file_path,
        subject,
        paraphrase,
        translate,
        correct_spelling,
        src,
        dest,
    ):
        """Send emails in buckets

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
        auth, _ = self.get_config()
        encrypted_emails = []
        message = get_file_content(message_file_path)
        #
        with tqdm(total=len(email_batches)) as filter_progress:
            for batch in email_batches:
                #
                plain_emails = batch
                #
                # TODO - send encrypted emails
                # get emails with gpg key in their own list
                # encrypted_emails = list(filter(lambda x: self.find_gpg_keyid(x), batch))
                # map(trace(lambda e, k: self.send_email(e, message, subject, do_paraphrase, translate_to_languagecode)), encrypted_emails)
                # plain_emails = list(filter(trace(lambda y: y not in encrypted_emails), batch))
                #
                if plain_emails:
                    print("sending email…")
                    self.send(
                        ";".join(plain_emails),
                        message,
                        subject,
                        paraphrase,
                        translate,
                        correct_spelling,
                        src,
                        dest,
                    )
                filter_progress.update(1)

    def send_batch(
        self,
        email_files_path,
        message_file_path,
        subject,
        paraphrase,
        translate,
        correct_spelling,
        src,
        dest,
    ):

        """Send Emails

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
        if not os.path.isfile(message_file_path):
            print("Invalid message file path!")
            status = 1
            return status
        #
        for ef in self.get_contact_files(email_files_path):
            email_list = get_file_content(ef)
            email_buckets = self.store_emails_in_buckets(email_list)
            self.send_emails_in_buckets(
                email_buckets,
                message_file_path,
                subject,
                paraphrase,
                translate,
                correct_spelling,
                src,
                dest,
            )
        #
        return status

    def send(
        self,
        mailing_list,
        message_content,
        subject,
        paraphrase=False,
        translate=False,
        correct_spelling=False,
        src=False,
        dest=False,
    ):
        """Send email
        Parameters
        ----------
        mailing_list : list
            The emails list
        message : MIMEMultipart
            The email messsage to send
        """
        status = 0
        auth, _ = self.get_config()
        print("send email > content file: " + json.dumps(message_content, indent=4))
        message = Compose.compose_email(
            auth["sender"],
            mailing_list,
            message_content,
            subject,
            paraphrase,
            translate,
            correct_spelling,
            src,
            dest,
        )
        if auth["security"] == "tls":
            try:
                print("Creating ssl context")
                context = ssl.create_default_context()
                print("Creating secure ssl/tls connection with server")
                with smtplib.SMTP_SSL(
                    auth["server"], auth["port"], context=context
                ) as server:
                    server.set_debuglevel(0)
                    print("Logging into server:" + json.dumps(auth, indent=4))
                    server.login(auth["user"], auth["password"])
                    print("Sending email")
                    error_status = server.sendmail(
                        auth["sender"], mailing_list, message.as_string()
                    )
                    print(error_status)
                    print("\x1b[6;37;42m Sent \x1b[0m")
                    server.quit()
            except Exception as err:
                print(f"\x1b[6;37;41m {type(err)} error occurred: {err}\x1b[0m")
                status = 1
        else:
            try:
                if auth["security"] == "starttls":
                    print("Creating ssl context")
                    context = ssl.create_default_context()
                print("Creating unsecure connection with server")
                with smtplib.SMTP(auth["server"], auth["port"]) as server:
                    server.set_debuglevel(0)
                    if auth["security"] == "starttls":
                        print("Upgrading unsecure connection with server with starttls")
                        server.ehlo()  # Can be omitted
                        server.starttls(context=context)  # Secure the connection
                        # server.ehlo() # Can be omitted
                    #
                    print("Logging into server")
                    server.login(auth["user"], auth["password"])
                    print("Sending email")
                    error_status = server.sendmail(
                        auth["sender"], mailing_list, message.as_string()
                    )
                    print("send status:" + json.dumps(error_status, indent=4))
                    print("\x1b[6;37;42m Sent \x1b[0m")
                    server.quit()
            except Exception as err:
                print(f"\x1b[6;37;41m {type(err)} error occurred: {err}\x1b[0m")
                status = 1
        #
        time.sleep(5)
        return status

    def send_envelope(
        self,
        mailing_list,
        message_content,
        subject,
        paraphrase=False,
        translate=False,
        correct_spelling=False,
        src=False,
        dest=False,
    ):
        """Send email

        Parameters
        ----------
        mailing_list : list
            The emails list
        message : MIMEMultipart
            The email messsage to send
        """
        status = 0
        auth, _ = self.get_config()
        html_content = Compose.md2html(message_content)
        # Create connection with server and send email
        try:
            # os.system(f'envelope --from {auth["sender"]} --to "{mailing_list}" --message "{html_content}" --smtp {auth["server"]} {auth["port"]} {auth["user"]} {auth["password"]} {auth["security"]} --send 1')
            msg = (
                Envelope()
                .header("Content-Type", "text/plain;charset=utf-8")
                .message(html_content)
                .subject(subject)
                .to(mailing_list)
                .from_(auth["sender"])
                .smtp(
                    host=auth["server"],
                    port=auth["port"],
                    user=auth["user"],
                    password=auth["password"],
                    security=auth["security"],
                    attempts=3,
                    delay=3,
                )
                .send(send=True, sign=None, encrypt=None)
            )

        except Exception as err:
            print(f"\x1b[6;37;41m {type(err)} error occurred: {err}\x1b[0m")
            status = 1
        #
        return status


class Riseup:

    """Parent class of mail program;

    Login credentials are optional, so user can decide to have persistent session or not;
    """

    SERVER = "mail.riseup.net"

    def __init__(self, user=None, pwd=None):
        self.user = user
        self.pwd = pwd
        self.loggedin = None
        # Status can be checked -> True / False

    def log_in(self):
        """Set Login credentials"""
        if not self.user or not self.pwd:
            user = input("\nYour Riseup username: ")
            pwd = getpass.getpass()
            # Set class parameters
            self.user = user
            self.pwd = pwd
            return
        else:
            return


class IMAP(Riseup):

    """IMAP4 protocol;

    Checking and reading mails;
    Different mail directories can be accessed and viewed;
    """

    port = "993"

    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)
        self.unseen_num = 0
        self.unseen_msg = []
        self.conn = imaplib.IMAP4_SSL(Riseup.SERVER, self.port)

    def connect(self):
        try:
            IMAP.conn.login(self.user, self.pwd)
            print("\n[+] Login successfull.\n")
            self.loggedin = True
            time.sleep(0.8)

        except:
            LOGGER.error("Error-Message")
            print("\n[!] There was an error logging you in.\n")
            self.loggedin = False

    def check_unread(self):
        """Checks if there are unseen msg in the Inbox;"""
        IMAP.conn.select()
        status, num = IMAP.conn.search(None, "UNSEEN")
        # Getting number of unread messages
        for n in num:
            self.unseen_num = len(n.decode("ascii").split())
        #
        if self.unseen_num > 0:
            print(f"There are {self.unseen_num} unseen messages.")
        else:
            print("\n\nThere are no new messages.")
            time.sleep(0.8)
        return

    def open_unread(self):
        """Prints out the unread messages;"""
        IMAP.conn.select()
        try:
            status, num = IMAP.conn.search(None, "UNSEEN")
            for x in range(self.unseen_num):
                for n in num[x].split():
                    typ, data = IMAP.conn.fetch(n, "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])
                #
                msg_size = len(msg.get_payload())
                print("\n---------------------------------------------------------")
                print("[+] From: ", msg["From"])
                print("[+] Subject: ", msg["Subject"])
                if msg_size == 1:
                    print("[+] Message: ", msg.get_payload())
                elif msg_size > 1:
                    for x in range(msg_size):
                        print("[+] Message: ", msg.get_payload[x])
                print("\n")
        #
        except:
            print("Couldn't open unread messages..")
        return

    def search_message(self):
        """User can search in chosen message directory for terms to find message;"""
        pass


class POP(Riseup):

    """Using POP3;"""

    port = "995"
    emails = []
    tries = 0
    fail_tries = 300
    subject = "Undelivered Mail Returned to Sender"
    month = "Jul 2018"
    not_found = 0
    total_emails = 0

    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)
        Mailbox = poplib.POP3_SSL("mail.privateemail.com")
        Mailbox.user("user@domain.com")
        Mailbox.pass_("pass")

    # Read dirty emails from emails.txt file
    def read_emails(self):
        print("Reading dirty emails...")
        print(
            "Script will exit after failing to read following Subject and Month \n\
    in parsed emails ",
            self.fail_tries,
            "times",
        )
        print("Subject : ", self.subject, "\nMonth : ", self.month)
        with open("emails.txt", "r") as f:
            self.emails = [line.strip() for line in f]
            self.total_emails = len(self.emails)

    # Write filtered emails to clean_emails.txt file
    def write_emails(self):
        print("Writing clean emails to file...")
        file = open("clean_emails.txt", "w")
        for e in self.emails:
            file.write(e + "\n")
        file.close()
        print("Done!")

    # Total inbox messages
    def get_total_emails(self):
        return len(self.Mailbox.list()[1])

    # Parse emails from mail text and filter dirty emails
    def filter_emails(self, total):
        #
        for i in reversed(range(total)):
            #
            raw_email = b"\n".join(self.Mailbox.retr(i + 1)[1])
            parsed_email = email.message_from_bytes(raw_email)
            #
            if (
                self.subject in parsed_email["Subject"]
                and self.month in parsed_email["Date"]
            ):
                #
                payload = parsed_email.get_payload()[0]
                body = payload.get_payload()
                match = re.search(r"[\w\.-]+@[\w\.-]+", body)
                remove_email = match.group(0).lstrip()
                try:
                    # print(parsed_email["Date"])
                    # print(parsed_email["Subject"])
                    # print('Remove', remove_email)
                    self.emails.remove(remove_email)
                except:
                    # print('Not Found', remove_email)
                    self.not_found += 1
                    pass
            else:
                self.tries += 1
            #
            if self.tries > self.fail_tries:
                print("Exiting after failing", self.fail_tries, "times")
                break

    def run(self):
        """ """
        self.read_emails()
        self.filter_emails(self.get_total_emails())
        self.write_emails()
        print("Total Emails Provided : ", self.total_emails)
        print("Filtered Emails : ", len(self.emails))
        print("Emails not found in emails.txt file : ", self.not_found)


class SMTP(Riseup):

    """Uses SMTP protocol for establishing

    the connection and transferring the message;
    Encryption and trace-deletion is handled here too;
    """

    port = "587"
    #

    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)
        self.msg = ""
        self.f = None
        self.recip = ""
        self._enc = None
        self.conn = smtplib.SMTP(Riseup.SERVER, self.port)

    def __call__(self):
        """After email was sent, all files can be overwritten and deleted;"""
        os.system(f"shred -uvz -n 30 {self.f}")
        os.system(f"shred -uvz -n 30 {self.enc}")
        return

    def set_recip(self):
        """Recipient needs to be set, so that encryption works properly;"""
        recip = input("\nEmail address of recipient: \n")
        self.recip = recip

    @classmethod
    def change_port(cls):
        """Normally port 587 is working, if not port 465 will be tried;"""
        cls.port = "587"
        return

    def connect(self):
        #
        try:
            SMTP.conn.starttls()
            print("\n[+] TLS Connection established\n")
            time.sleep(0.8)
            SMTP.conn.login(self.user, self.pwd)
            self.loggedin = True
            print("\n[+] Login successfull\n")
            time.sleep(0.8)
        except:
            LOGGER.error("Error-Message")
            print("[!] Connection could not be established.")
            self.loggedin = False
        #
        return

    def sendmail(self):
        """Is sending message if a connection could be established before;"""

        # Riseup just accepts MIME;
        from email.mime.text import MIMEText

        # Own Email address
        my_mail = self.user + "@riseup.net"
        # Define the MIME Format;
        msg = MIMEText(self.msg)
        msg["From"] = my_mail
        msg["To"] = self.recip
        msg["Subject"] = input("Subject of Mail: [can be empty] \n")
        #
        try:
            SMTP.conn.send_message(msg)
            time.sleep(0.5)
            print("\n\n[+] Email successfull sent.\n")
            print("Returning to the Main Menu")
            time.sleep(0.8)
        except:
            LOGGER.error("Error-Message")
            print("\n[!] Something went wrong\n")
        #
        return

    def get_text(self):
        """Gets the message which will be sent;

        Choosing between write message directly, or read message from f;
        """
        try:
            opt = input("\nWrite message or read from file? (w/r)  : \n")
            if opt == "w":
                t = input("Your message to be sent: ")
            elif opt == "r":
                self.f = input("\nSpecify file (&path): \n")
                with open(self.f, "r") as f:
                    t = f.read()
            # Class variable which will be sent;
            self.msg = t
        except:
            LOGGER.error("Error-Message")
            print("\n[!] Couldn't write text to message.\n")
        return

    def encrypt_msg(self):
        """Encrypts the message;

        Just working with files until now;
        """
        # Specify file (and Path)
        self.f = input("File (+Path) to encrypt: ")
        os.system(f"gpg --encrypt -a --recipient {self.recip} {self.f}")
        self.enc = self.f + ".asc"
        return

    def end_connect(self):
        # End conncetion
        SMTP.conn.close()


# Not ready to use yet !
class Canary:

    """Downloading the canary statement of Riseup to verify it is still safe to use;

    -- Recommended: --
    Read more about:
    << https://riseup.net/en/canary >>
    """

    LINK = "https://riseup.net/en/canary"
    KEYSERVER = "keys.riseup.net"
    FINGERPRINT = "0x4E0791268F7C67EABE88F1B03043E2B7139A768E"
    KEY = "RiseupCanary.key"
    CANARYSIGN = "riseup.net/ceritificates/riseup-signed-certificate-fingerprints.txt"
    CANARYLINK = "https://riseup.net/about-us/canary/canary-statement-signed.txt"
    CANARY = "canary-statement-signed.txt"

    @classmethod
    def verify_pubkey(cls):
        """Public Keys are gonna

        downloaded and certificates can be read;
        GPG must be installed on user's OS;
        """
        print(
            """\n
        ======================================================================
        Warning! If you are not familiar with this
        visit: https://riseup.net/en/security/network-security/certificates
        ======================================================================
        \n"""
        )
        time.sleep(1)
        os.system(f"gpg --keyserver {cls.KEYSERVER} --recv-key {cls.FINGERPRINT}")
        os.system(f"gpg --fingerprint {cls.FINGERPRINT}")
        # Optional
        os.system(f"gpg --list-sigs {cls.FINGERPRINT}")

        return

    @classmethod
    def verify_statement(cls):
        """Canary Statement is verified here;"""
        # Load statement
        os.system(f"wget {cls.CANARYLINK}")
        # Verify
        os.system(f"gpg --auto-key-retrieve --verify {cls.CANARY}")
        # Open Statement (optional)
        ask = input("\n\nDo you want to see the statement? ")
        if ask == "y" or ask == "yes":
            with open(cls.CANARY, "r") as statement:
                st = statement.read()
            print(st)
        else:
            pass
        return

    @classmethod
    def del_all(cls):
        """User can decide if files will be overwritten and deleted;"""
        os.system(f"shred -uvz -n 30 {cls.CANARY}")
        # os.system(f'shred -uvz -n 30 {}')

        return
