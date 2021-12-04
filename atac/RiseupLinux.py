#####################################################
# Email Program for Riseup users                    #
# This program is free and OpenSource               #
#                                                   #
#                                                   #
# OS: Linux                                         #
# Enryption just possible on Linux distributions    #
#                                                   #
# @m1ghtfr3e                                        #
#####################################################

import os
import time
import imaplib
import poplib
import smtplib
import getpass
import email
import base64
import logging


# Logging
## For results: open << debug.log >>
LOGGER = logging.getLogger('Riseup_Log')
LOGGER.setLevel(logging.DEBUG)
fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
LOGGER.addHandler(fh)
#LOGGER.debug('Debug-Message')
#LOGGER.info('Info-Message')
#LOGGER.warning('Warning-message')
#LOGGER.error('Error-Message')

#########################################################################################
#                                         A                                             #
#########################################################################################

class Riseup:

    '''
    Parent class of mail
    program;
    Login credentials are
    optional, so user can
    decide to have persistent
    session or not;
    '''
    
    SERVER = 'mail.riseup.net'

    def __init__(self, user=None, pwd=None):
        self.user = user
        self.pwd = pwd
        self.loggedin = None        # Status can be checked -> True / False

    def log_in(self):
        '''
        Set Login credentials
        '''

        if self.user == None and self.pwd == None:
            user = input('\nYour Riseup username: ')
            pwd = getpass.getpass()

            # Set class parameters
            self.user = user
            self.pwd = pwd
            return
        else:
            return


class IMAP(Riseup):

    '''
    IMAP4 protocol;
    Checking and 
    reading mails;
    Different mail
    directories can
    be accessed and
    viewed;
    '''

    port = '993'
    conn = imaplib.IMAP4_SSL(Riseup.SERVER, port)
    
    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)
        self.unseen_num = 0
        self.unseen_msg = []

    def connect(self):
        try:
            IMAP.conn.login(self.user, self.pwd)
            print('\n[+] Login successfull.\n')
            self.loggedin = True
            time.sleep(.8)

        except:
            LOGGER.error('Error-Message')
            print('\n[!] There was an error logging you in.\n')
            self.loggedin = False

    def check_unread(self):
        '''
        Checks if there
        are unseen msg 
        in the Inbox;
        '''
        IMAP.conn.select()
        status, num = IMAP.conn.search(None, 'UNSEEN')
        # Getting number of unread messages
        for n in num:
            self.unseen_num = len(n.decode('ascii').split())
       
        if self.unseen_num > 0:
            print(f'There are {self.unseen_num} unseen messages.')
        else:
            print('\n\nThere are no new messages.')
            time.sleep(.8)
        return

    def open_unread(self):
        '''
        Prints out the unread
        messages;
        '''
        IMAP.conn.select()
        try:
            status, num = IMAP.conn.search(None, 'UNSEEN')            
            for x in range(self.unseen_num):
                for n in num[x].split():
                    typ, data = IMAP.conn.fetch(n, '(RFC822)')

                    msg = email.message_from_bytes(data[0][1])
                
                msg_size = len(msg.get_payload())

 
                print('\n---------------------------------------------------------')
                print('[+] From: ', msg['From'])
                print('[+] Subject: ', msg['Subject'])
                if msg_size == 1:
                    print('[+] Message: ', msg.get_payload())
                elif msg_size > 1:
                    for x in range(msg_size):
                        print('[+] Message: ', msg.get_payload[x])
                print('\n')

        except:
            print('Couldn\'t open unread messages..')
        return            

    def search_message(self):
        '''
        User can search
        in chosen message
        directory for terms
        to find message;
        '''
        pass


class POP(Riseup):

    '''
    Using POP3;
    '''


    port = '995'

    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)


class SMTP(Riseup):

    '''
    Uses SMTP protocol
    for establishing 
    the connection and
    transferring the
    message;
    Encryption and 
    trace-deletion is
    handled here too;
    '''

    port = '587'
    conn = smtplib.SMTP(Riseup.SERVER, port)
    
    def __init__(self, user=None, pwd=None):
        super().__init__(user, pwd)
        self.msg = ''
        self.f = None
        self.recip = ''
        self._enc = None
    
    def __call__(self):
        '''
        After email was sent,
        all files can be 
        overwritten and deleted;
        '''
        os.system(f'shred -uvz -n 30 {self.f}')
        os.system(f'shred -uvz -n 30 {self.enc}')
        return

    def set_recip(self):
        '''
        Recipient needs to
        be set, so that
        encryption works
        properly;
        '''
        recip = input('\nEmail address of recipient: \n')
        self.recip = recip

    @classmethod
    def change_port(cls):
        '''
        Normally port 587 
        is working, if not
        port 465 will be
        tried;
        '''
        cls.port = '587'
        return

    def connect(self):

        try:
            SMTP.conn.starttls()
            print('\n[+] TLS Connection established\n')
            time.sleep(.8)
            SMTP.conn.login(self.user, self.pwd)
            self.loggedin = True
            print('\n[+] Login successfull\n')
            time.sleep(.8)
            
        except:
            LOGGER.error('Error-Message')
            print('[!] Connection could not be established.')
            self.loggedin = False
        return

    def sendmail(self):
        '''
        Is sending message
        if a connection could
        be established before;
        '''
        # Riseup just accepts MIME;
        from email.mime.text import MIMEText

        # Own Email address
        my_mail = self.user + '@riseup.net'

        # Define the MIME Format;
        msg = MIMEText(self.msg)
        msg['From'] = my_mail
        msg['To'] = self.recip
        msg['Subject'] = input('Subject of Mail: [can be empty] \n')

        try:
            SMTP.conn.send_message(msg)
            time.sleep(.5)
            print('\n\n[+] Email successfull sent.\n')
            print('Returning to the Main Menu')
            time.sleep(.8)
        except:
            LOGGER.error('Error-Message')
            print('\n[!] Something went wrong\n')

        return

    def get_text(self):
        '''
        Gets the message which
        will be sent;
        Choosing between write
        message directly, 
        or read message from f;
        '''

        try:
            opt = input('\nWrite message or read from file? (w/r)  : \n')
            if opt == 'w':
                t = input('Your message to be sent: ')
            elif opt == 'r':
                self.f = input('\nSpecify file (&path): \n')
                with open(self.f, 'r') as f:
                    t = f.read()
            # Class variable which will be sent;
            self.msg = t
        except:
            LOGGER.error('Error-Message')
            print('\n[!] Couldn\'t write text to message.\n')
        return

    def encrypt_msg(self):
        '''
        Encrypts the
        message;
        Just working with
        files until now;
        '''
        # Specify file (and Path)
        self.f = input('File (+Path) to encrypt: ')
        os.system(f'gpg --encrypt -a --recipient {self.recip} {self.f}')
        self.enc = self.f + '.asc'
        return

    def end_connect(self):
        # End conncetion
        SMTP.conn.close()


# Not ready to use yet !
class Canary:

    '''
    Downloading the
    canary statement
    of Riseup to verify
    it is still safe
    to use;
    -- Recommended: --
    Read more about:
    << https://riseup.net/en/canary >>
    '''
    
    LINK = 'https://riseup.net/en/canary'
    KEYSERVER = 'keys.riseup.net'
    FINGERPRINT = '0x4E0791268F7C67EABE88F1B03043E2B7139A768E'
    KEY = 'RiseupCanary.key'
    CANARYSIGN = 'riseup.net/ceritificates/riseup-signed-certificate-fingerprints.txt'
    CANARYLINK = 'https://riseup.net/about-us/canary/canary-statement-signed.txt'
    CANARY = 'canary-statement-signed.txt'

    @classmethod
    def verify_pubkey(cls):
        '''
        Public Keys are gonna
        downloaded and 
        certificates can be
        read;
        GPG must be installed
        on user's OS;
        '''
        print('''\n
        ======================================================================
        Warning! If you are not familiar with this 
        visit: https://riseup.net/en/security/network-security/certificates
        ======================================================================
        \n''')
        time.sleep(1)
        os.system(f'gpg --keyserver {cls.KEYSERVER} --recv-key {cls.FINGERPRINT}')
        os.system(f'gpg --fingerprint {cls.FINGERPRINT}')
        # Optional
        os.system(f'gpg --list-sigs {cls.FINGERPRINT}')

        return

    @classmethod
    def verify_statement(cls):
        '''
        Canary Statement
        is verified here;
        '''
        
        # Load statement
        os.system(f'wget {cls.CANARYLINK}')

        # Verify
        os.system(f'gpg --auto-key-retrieve --verify {cls.CANARY}')

        # Open Statement (optional)
        ask = input('\n\nDo you want to see the statement? ')
        if ask == 'y' or ask == 'yes':
            with open(cls.CANARY, 'r') as statement:
                st = statement.read()
            print(st)
        else:
            pass
        return

    @classmethod
    def del_all(cls):
        '''
        User can decide
        if files will be
        overwritten and
        deleted;
        '''
        os.system(f'shred -uvz -n 30 {cls.CANARY}')
        #os.system(f'shred -uvz -n 30 {}')
        
        return