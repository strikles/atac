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
        print(email)
        is_valid = validate_email(email)
        return is_valid
                                  
    def cleanup(self, path):
        
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
                                print('VALID')
                                ml_emails[ml_counter // 2000].append(receiver_email)
                                ml_counter += 1
                            else:
                                print('{0} INVALID'.format(receiver_email))
                        progress.update(1)
                        