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


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """
    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
                return cls._instances[cls]


class Config(metaclass=SingletonMeta):

    def __init__(self):
        self.key = None
        self.data = None
        if not os.path.isfile('auth.json'):
            self.new_config()
        else:
            self.load_config()

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
        if not self.key:
            self.key = self.generate_key()
        fernet = Fernet(self.key) 
        # encrypting the file 
        encrypted = fernet.encrypt(json.dumps(self.data, ensure_ascii=False).encode('utf8'))
        # opening the file in write mode and writing the encrypted data 
        with open('auth.json', 'wb') as encrypted_file: 
            encrypted_file.write(encrypted) 

    def load_config(self):
        if not self.key:
            self.key = self.generate_key()
        fernet = Fernet(self.key)
        # opening the encrypted file 
        with open('auth.json', 'rb') as enc_file: 
            encrypted = enc_file.read() 
        # decrypting the file 
        self.data = json.loads(json.dumps(fernet.decrypt(encrypted), ensure_ascii=False).decode('utf8'))
        print(self.data)

    def load_decrypted(self):
        with open('new.json', 'rb') as new_config: 
            self.data = json.loads(new_config.read())