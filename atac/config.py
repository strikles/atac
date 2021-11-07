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

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        self.key = None
        self.data = None
        self.encrypted_config = encrypted_config
        self.config_file_path = config_file_path
        self.key_file_path = key_file_path
        #
        if self.key_file_path:
            self.load_key(self.key_file_path)
        if not self.key:
            self.generate_key()
        #
        if not os.path.isfile(self.config_file_path):
            self.new_config(self.config_file_path, self.encrypted_config)
        self.load_config()
        #
        my_art = ascii_magic.from_image_file(
            img_path="assets/img/IMG_3339.JPG",
            columns=80,
            mode=ascii_magic.Modes.TERMINAL
        )
        ascii_magic.to_terminal(my_art)

    def generate_key(self):
        # key generation 
        #self.key = Fernet.generate_key()
        if "PYTEST_CURRENT_TEST" in os.environ:
            password =  bytes("M4m4k154n", encoding='utf8')
            salt = bytes("77", encoding='utf8')
        else:
            password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), 'utf-8')
            salt = bytes(stdiomask.getpass(prompt='Enter Salt (leave blank if not required) - ', mask='*'), 'utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password))

    def load_key(self, key_file_path):
        with open(key_file_path, 'wb') as key_file: 
            self.key = key_file.read()

    def save_key(self, key_file_path):
        with open(key_file_path, 'wb') as key_file: 
            key_file.write(self.key) 

    def new_config(self, config_file_path):
        with open('new.json', 'rb') as new_config: 
            self.data = json.loads(new_config.read())
        self.save_config(config_file_path, True)

    def save_config(self, config_file_path, encrypted_config):
        if encrypted_config:
            fernet = Fernet(self.key) 
            # encrypting the file 
            encrypted_data = fernet.encrypt(json.dumps(self.data, ensure_ascii=False).encode('utf8'))
            # opening the file in write mode and writing the encrypted data 
            with open(config_file_path, 'wb') as encrypted_file: 
                encrypted_file.write(encrypted_data) 
        else:
            with open(config_file, 'wb') as unencrypted_file: 
                unencrypted_file.write(self.data, ensure_ascii=False)

    def load_config(self):
        if self.encrypted_config:
            fernet = Fernet(self.key)
            # opening the encrypted file 
            with open(self.config_file, 'rb') as enc_file: 
                encrypted_data = enc_file.read() 
            # decrypting the file 
            try:
                self.data = json.loads(fernet.decrypt(encrypted_data))
            except InvalidToken as e:
                print("Invalid Key - Unsuccessfully decrypted")
                sys.exit(1)
        else:
            with open(self.config_file, 'rb') as new_config: 
                self.data = json.loads(new_config.read())
