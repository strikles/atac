import os
import sys
import json
import stdiomask
from threading import Lock, Thread
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import ascii_magic


class Config:

    def __init__(self):
        self.key = None
        self.data = None
        if not self.key:
            self.key = self.generate_key()
        if not os.path.isfile('auth.json'):
            self.new_config()
        self.load_config()
        my_art = ascii_magic.from_image_file(
            img_path="assets/img/IMG_3331.PNG",
            columns=80,
            mode=ascii_magic.Modes.TERMINAL
        )
        ascii_magic.to_terminal(my_art)

    def generate_key(self):
        # key generation 
        #self.key = Fernet.generate_key()
        if "PYTEST_CURRENT_TEST" in os.environ:
            password =  bytes("abcefghik", encoding='utf8')
            salt = bytes("123", encoding='utf8')
        else:
            password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), 'utf-8')
            salt = bytes(stdiomask.getpass(prompt='Enter Salt (leave blank if not required) - ', mask='*'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        return base64.urlsafe_b64encode(kdf.derive(password))

    def new_config(self):
        self.load_decrypted()
        self.save_config()

    def save_config(self):
        fernet = Fernet(self.key) 
        # encrypting the file 
        encrypted = fernet.encrypt(json.dumps(self.data, ensure_ascii=False).encode('utf8'))
        # opening the file in write mode and writing the encrypted data 
        with open('auth.json', 'wb') as encrypted_file: 
            encrypted_file.write(encrypted) 

    def load_config(self):
        fernet = Fernet(self.key)
        # opening the encrypted file 
        with open('auth.json', 'rb') as enc_file: 
            encrypted = enc_file.read() 
        # decrypting the file 
        self.data = json.loads(fernet.decrypt(encrypted))

    def load_decrypted(self):
        with open('new.json', 'rb') as new_config: 
            self.data = json.loads(new_config.read())