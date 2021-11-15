import os
import sys
import json
import gnupg
import stdiomask
from threading import Lock, Thread
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import inspect


class Config(object):

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        self.key = None
        self.data = None
        self.encrypted_config = encrypted_config
        self.config_file_path = config_file_path
        self.key_file_path = key_file_path
        self.gpg = gnupg.GPG(homedir='~/.gnupg')
        #
        if encrypted_config and self.key_file_path:
            self.load_key(self.key_file_path)
            print(self.key)
        if encrypted_config and not self.key:
            self.generate_key()
        #
        if not os.path.isfile(self.config_file_path):
            self.new_config(self.config_file_path, self.encrypted_config)
        self.load_config()

    def generate_key(self):
        # key generation
        print(inspect.stack()[1].function)
        if "PYTEST_CURRENT_TEST" in os.environ:
            password = bytes("M4m4k154n", encoding='utf-8')
            salt = bytes("77", encoding='utf-8')
        else:
            password = bytes(stdiomask.getpass(prompt='\nEnter password - ', mask='*'), encoding='utf-8')
            salt = bytes(stdiomask.getpass(prompt='Enter Salt (optional) - ', mask='*'), encoding='utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend())
        self.key = base64.urlsafe_b64encode(kdf.derive(password))

    def load_key(self, key_file_path):
        #
        try:
            with open(key_file_path, 'rb') as key_file:
                self.key = key_file.read()
        except OSError as e:
            print('{} file error {}'.format(key_file_path, e.errno))
        finally:
            key_file.close()

    def save_key(self, key_file_path):
        #
        try:
            with open(key_file_path, 'wb') as key_file:
                key_file.write(self.key)
        except OSError as e:
            print('{} file error {}'.format(key_file_path, e.errno))
        finally:
            key_file.close()

    def new_config(self, config_file_path):
        #
        try:
            with open('new.json', 'rb') as new_config:
                self.data = json.loads(new_config.read())
        except OSError as e:
            print('{} file error {}'.format('new.json', e.errno))
        finally:
            new_config.close()
        #
        self.save_config(config_file_path, True)

    def save_config(self, config_file_path, encrypted_config):
        #
        if encrypted_config:
            fernet = Fernet(self.key)
            # encrypting the file
            encrypted_data = fernet.encrypt(json.dumps(self.data, ensure_ascii=False).encode('utf8'))
            # opening the file in write mode and writing the encrypted data
            try:
                with open(config_file_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data)
            except OSError as e:
                print('{} file error {}'.format(config_file_path, e.errno))
            finally:
                encrypted_file.close()
        else:
            try:
                with open(config_file_path, 'wb') as unencrypted_file:
                    unencrypted_file.write(self.data, ensure_ascii=False)
            except OSError as e:
                print('{} file not found {}'.format(config_file_path, e.errno))
            finally:
                unencrypted_file.close()

    def load_config(self):
        #
        if self.encrypted_config:
            fernet = Fernet(self.key)
            # opening the encrypted file
            try:
                with open(self.config_file_path, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()
            except OSError as e:
                print('{} file error {}'.format(self.config_file_path, e.errno))
            finally:
                encrypted_file.close()
            # decrypting the file
            try:
                self.data = json.loads(fernet.decrypt(encrypted_data))
            except InvalidToken as e:
                print("Invalid Key {} - Unsuccessfully decrypted").format(e)
                sys.exit(1)
        else:
            try:
                with open(self.config_file_path, 'rb') as new_config:
                    self.data = json.loads(new_config.read())
            except OSError as e:
                print('{} file error {}'.format(self.config_file_path, e.errno))
            finally:
                new_config.close()
