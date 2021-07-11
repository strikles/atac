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

    def valid_email(self, email):
        auth_ndx = self.config['send']['email']['active_auth']
        auth = self.config['send']['email']['auth'][auth_ndx]
        print(email)
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
                                  
    def clean_files(self, path):
        
        print(path)
        status = 0
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
        
        for ml in ml_files:
            cf = path + ml
            print(cf)
            with open(cf) as file:
                
                lines = [line for line in file]
                ml_emails = [[] for i in range((len(lines) // 2000) + 1)]
                ml_counter = 0

                with tqdm(total=len(lines)) as progress:
                    for ndx, receiver_email in csv.reader(lines):
                        if checkers.is_email(receiver_email):
                            if self.valid_email(receiver_email):    
                                ml_emails[ml_counter // 2000].append(receiver_email)
                                ml_counter += 1
                        progress.update(1)
                        