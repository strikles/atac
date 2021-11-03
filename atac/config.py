import os
import sys
import json
from cryptography.fernet import Fernet


class Config:


    def __init__(self):
        self.key = None
        self.data = None
        if not os.path.isfile('filekey.key'):
            self.gen_key()
        if not os.path.isfile('auth.json'):
            self.new_config()
        else:
            self.load_config()
        #print(self.data)


    def gen_key(self):
        # key generation 
        self.key = Fernet.generate_key() 
        # string the key in a file 
        with open('filekey.key', 'wb') as filekey: 
            filekey.write(self.key)

            
    def new_config(self):
        with open('new.json', 'rb') as new_config: 
            self.data = new_config.read()
        self.save_config()


    def save_config(self):
        # opening the key 
        with open('filekey.key', 'rb') as filekey: 
            self.key = filekey.read() 
        # using the generated key 
        fernet = Fernet(self.key) 
        # encrypting the file 
        encrypted = fernet.encrypt(self.data) 
        # opening the file in write mode and  
        # writing the encrypted data 
        with open('auth.json', 'wb') as encrypted_file: 
            encrypted_file.write(encrypted) 


    def load_config(self):
        with open('filekey.key', 'rb') as filekey: 
            self.key = filekey.read() 
        # using the key 
        fernet = Fernet(self.key) 
        # opening the encrypted file 
        with open('auth.json', 'rb') as enc_file: 
            encrypted = enc_file.read() 
        # decrypting the file 
        self.data = json.loads(fernet.decrypt(encrypted))


    def load_decrypted(self):
        with open('new.json', 'rb') as new_config: 
            self.data = new_config.read() 