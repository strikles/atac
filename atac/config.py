import os
import sys
import json
import stdiomask
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Config:

    def __init__(self):
        self.key = None
        self.data = None
        if not os.path.isfile('auth.json'):
            self.new_config()
        else:
            self.load_config()

    def gen_key(self):
        # key generation 
        #self.key = Fernet.generate_key()
        password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), 'utf-8')
        salt = bytes(stdiomask.getpass(prompt='Enter Salt (leave blank if not required) - ', mask='*'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password))

    def new_config(self):
        with open('new.json', 'rb') as new_config: 
            self.data = new_config.read()
        self.save_config()

    def save_config(self):
        password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), 'utf-8')
        salt = bytes(stdiomask.getpass(prompt='Enter Salt (leave blank if not required) - ', mask='*'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password)) 
        fernet = Fernet(self.key) 
        # encrypting the file 
        encrypted = fernet.encrypt(self.data) 
        # opening the file in write mode and writing the encrypted data 
        with open('auth.json', 'wb') as encrypted_file: 
            encrypted_file.write(encrypted) 

    def load_config(self):
        password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), 'utf-8')
        salt = bytes(stdiomask.getpass(prompt='Enter Salt (leave blank if not required) - ', mask='*'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password)) 
        fernet = Fernet(self.key) 
        # opening the encrypted file 
        with open('auth.json', 'rb') as enc_file: 
            encrypted = enc_file.read() 
        # decrypting the file 
        self.data = json.loads(fernet.decrypt(encrypted))

    def load_decrypted(self):
        with open('new.json', 'rb') as new_config: 
            self.data = new_config.read() 