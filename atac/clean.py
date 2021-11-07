import os
import sys
import smtplib
import csv
import json
import time
from validator_collection import checkers

from tqdm import tqdm
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException, phonenumberutil

from .config import Config


class Leon(Config):
    #
    FIXED_LINE = 0
    MOBILE = 1
    # In some regions (e.g. the USA), it is impossible to distinguish between
    # fixed-line and mobile numbers by looking at the phone number itself.
    FIXED_LINE_OR_MOBILE = 2
    # Freephone lines
    TOLL_FREE = 3
    PREMIUM_RATE = 4
    # The cost of this call is shared between the caller and the recipient,
    # and is hence typically less than PREMIUM_RATE calls. See
    # http://en.wikipedia.org/wiki/Shared_Cost_Service for more information.
    SHARED_COST = 5
    # Voice over IP numbers. This includes TSoIP (Telephony Service over IP).
    VOIP = 6
    # A personal number is associated with a particular person, and may be
    # routed to either a MOBILE or FIXED_LINE number. Some more information
    # can be found here: http://en.wikipedia.org/wiki/Personal_Numbers
    PERSONAL_NUMBER = 7
    PAGER = 8
    # Used for "Universal Access Numbers" or "Company Numbers". They may be
    # further routed to specific offices, but allow one number to be used for
    # a company.
    UAN = 9
    # Used for "Voice Mail Access Numbers".
    VOICEMAIL = 10
    # A phone number is of type UNKNOWN when it does not fit any of the known
    # patterns for a specific region.
    UNKNOWN = 99
    
    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        super().__init__(encrypted_config, config_file_path, key_file_path)

    def clean_phones(self, path):
        print(path)
        status = 0
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        for ml in ml_files:
            cf = path + ml
            print(cf)
            #read
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
                                print(line_type)
                        except NumberParseException as e:
                            print(str(e))

    def valid_email(self, email):
        is_valid = False
        try:
            # Validate.
            is_valid = validate_email(email)
            # Update with the normalized form.
            email = is_valid.email
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
        return is_valid

    def clean_emails(self, path):
        print(path)
        status = 0
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        for ml in ml_files:
            cf = path + ml
            print(cf)
            ml_emails = []
            #read
            with open(cf) as file:
                lines = [line for line in file]
                with tqdm(total=len(lines)) as progress:
                    for ndx, receiver_email in csv.reader(lines):
                        if self.valid_email(receiver_email):
                            ml_emails.append({'index': ndx, 'email': receiver_email})
                        else:
                            print('{0} INVALID'.format(receiver_email))
                        progress.update(1)
            # write
            with open(cf, mode='a') as file2:
                file2.truncate(0)
                with tqdm(total=len(ml_emails)) as progress2:
                    writer = csv.writer(file2,
                                        delimiter=',',
                                        quotechar='"',
                                        quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(['', 'email'])
                    for item in ml_emails:
                        writer.writerow([item['index'], item['email']])
                        progress2.update(1)
