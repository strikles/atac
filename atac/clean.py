import os
import sys
import smtplib
import csv
import json
import time
from validator_collection import checkers

from tqdm import tqdm
from email_validator import validate_email, EmailNotValidError


class Leon:
    
    def __init__(self):
        self.config = {}
        with open('auth.json') as json_file:
            self.config = json.load(json_file)
            
    def get_phone_type(content):
        
            
    def valid_mobile():
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
                        #build url
                        url = "https://libphonenumber.appspot.com/phonenumberparser?number=%2B"
                        try:
                            response = requests.get(url, timeout=10, stream=False)
                            response.encoding = "utf-8"
                            # If the response was successful, no Exception will be raised
                            response.raise_for_status()
                        except HTTPError as http_err:
                            print(f'HTTP error occurred: {http_err}')
                            continue
                        except Exception as err:
                            print(f'Other error occurred: {err}')
                            continue
                        else:
                            pass
                        phone_type = self.get_phone_type(response.text)

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

    def cleanup(self, path):
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