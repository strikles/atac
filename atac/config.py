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
from PIL import Image
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
            path="assets/img/IMG_3332.JPG",
            columns=200,
            width_ratio=2,
            mode=ascii_magic.Modes.HTML
        )
        ascii_magic.to_terminal(my_art)
        
    def colete_voador(self, image_path):
        # pass the image as command line argument
        img = Image.open(image_path)
        # resize the image
        width, height = img.size
        aspect_ratio = height/width
        new_width = 80
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))
        # new size of image
        # print(img.size)
        # convert image to greyscale format
        img = img.convert('L')
        pixels = img.getdata()
        # replace each pixel with a character from array
        chars = ["B","S","#","&","@","$","%","*","!",":","."]
        new_pixels = [chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        # split string of chars into multiple strings of length equal to new width and create a list
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        print(ascii_image)

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