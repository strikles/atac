import os
import sys
import smtplib
import csv
import json
import time
from validator_collection import checkers

from tqdm import tqdm
from validate_email import validate_email


class Leon:
    
    def __init__(self):
        self.config = {}
        with open('auth.json') as json_file:
            self.config = json.load(json_file)

    def valid_email(self, email):
        auth_ndx = self.config['send']['email']['active_auth']
        auth = self.config['send']['email']['auth'][auth_ndx]
        is_valid = validate_email(email_address=email, 
                                  check_format=True, 
                                  check_blacklist=True, 
                                  check_dns=True, 
                                  dns_timeout=10, 
                                  check_smtp=True, 
                                  smtp_timeout=10, 
                                  smtp_helo_host=auth['server'], 
                                  smtp_from_address=auth['sender'], 
                                  smtp_debug=False)
                                  
        return is_valid
                                  
    def cleanup(self, path):
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
                ml_emails = []
                with tqdm(total=len(lines)) as progress:
                    for ndx, receiver_email in csv.reader(lines):
                        if checkers.is_email(receiver_email):
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