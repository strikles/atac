from .Send import Send

import os
import random
import sys
import time

from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mregex_handler import MRegexHandler
from matrix_bot_api.mcommand_handler import MCommandHandler

#import phonenumbers
from phonenumbers import NumberParseException, phonenumberutil

if os.environ.get('DISPLAY'):
    from pywhatkit import *

class SendChat(Send):
    """ A class used to represent a Configuration object

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
    """

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        """ Class init

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
        self.chat = self.data['chat']

    # Global variables
    USERNAME = ""  # Bot's username
    PASSWORD = ""  # Bot's password
    SERVER = ""  # Matrix server URL


    def hi_callback(room, event):
        # Somebody said hi, let's say Hi back
        room.send_text("Hi, " + event['sender'])


    def echo_callback(room, event):
        args = event['content']['body'].split()
        args.pop(0)
        # Echo what they said back
        room.send_text(' '.join(args))


    def dieroll_callback(room, event):
        # someone wants a random number
        args = event['content']['body'].split()
        # we only care about the first arg, which has the die
        die = args[0]
        die_max = die[2:]
        # ensure the die is a positive integer
        if not die_max.isdigit():
            room.send_text('{} is not a positive number!'.format(die_max))
            return
        # and ensure it's a reasonable size, to prevent bot abuse
        die_max = int(die_max)
        if die_max <= 1 or die_max >= 1000:
            room.send_text('dice must be between 1 and 1000!')
            return
        # finally, send the result back
        result = random.randrange(1,die_max+1)
        room.send_text(str(result))


    def send_matrix(self):
        # Create an instance of the MatrixBotAPI
        bot = MatrixBotAPI(self.USERNAME, self.PASSWORD, self.SERVER)
        # Add a regex handler waiting for the word Hi
        hi_handler = MRegexHandler("Hi", self.hi_callback)
        bot.add_handler(hi_handler)
        # Add a regex handler waiting for the echo command
        echo_handler = MCommandHandler("echo", self.echo_callback)
        bot.add_handler(echo_handler)
        # Add a regex handler waiting for the die roll command
        dieroll_handler = MCommandHandler("d", self.dieroll_callback)
        bot.add_handler(dieroll_handler)
        # Start polling
        bot.start_polling()


    if os.environ.get('DISPLAY'):
        def send_pywhatkit(self, contacts_file_path, message_file_path):
            """ Send Pywhatkit message

            Parameters
            ----------
            contacts_file_path : str
                The path to the phone numbers CSV
            message_file_path : str
                The path to the message file
            """
            msg = '\n'.join(self.get_file_content(message_file_path, 'message'))
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
        """ Send Signal message

        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        """

        """
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

    def send(self):
        pass