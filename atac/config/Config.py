import os
import sys
import json
import gnupg
import stdiomask
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import inspect


class Config:
    """A class used to represent a Configuration object

    Attributes
    ----------
    key : str
        a encryption key
    data : dict
        configuration data
    encrypted_config : bool
        use an encrypted configuration file
    config_file_path : str
        path to the configuration file
    key_file_path : str
        path to encryption key file
    gpg : gnupg.GPG
        python-gnupg gnupg.GPG

    Methods
    -------
    generate_key()
        Generates a new encryption key from a password + salt

    """

    def __init__(self, encrypted_config=True, config_file_path="auth.json", key_file_path=None):
        """Class init

        Parameters
        ----------
        encrypted_config : bool
            use an encrypted configuration file
        config_file_path : str
            path to the configuration file
        key_file_path : str
            path to encryption key file
        """
        self.key = None
        self.data = None
        self.encrypted_config = encrypted_config
        self.config_file_path = config_file_path
        self.key_file_path = key_file_path
        self.gpg = gnupg.GPG()
        #
        if encrypted_config and self.key_file_path:
            self.load_key(self.key_file_path)
            print(self.key)
        #
        if encrypted_config and not self.key:
            self.generate_key()
        #
        if not os.path.isfile(self.config_file_path):
            self.new_config(self.config_file_path)
        #
        self.load_config()

    def generate_key(self):
        """Generates encryption key from password + salts"""

        print(inspect.stack()[1].function)
        if "PYTEST_CURRENT_TEST" in os.environ:
            password = bytes("M4m4k154n", encoding="utf-8")
            salt = bytes("77", encoding="utf-8")
        else:
            password = bytes(
                stdiomask.getpass(prompt="\nEnter password - ", mask="*"),
                encoding="utf-8",
            )
            salt = bytes(
                stdiomask.getpass(prompt="Enter Salt (optional) - ", mask="*"),
                encoding="utf-8",
            )
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password))

    def load_key(self, key_file_path):

        """Load encryption key file

        Parameters
        ----------
        key_file_path : str
            path to encryption key file
        """
        try:
            with open(key_file_path, "rb") as key_file:
                self.key = key_file.read()
        except OSError as e:
            print("{} file error {}".format(key_file_path, e.errno))

    def save_key(self, key_file_path):
        """Save encryption key file

        Parameters
        ----------
        key_file_path : str
            path to encryption key file
        """
        try:
            with open(key_file_path, "wb") as key_file:
                key_file.write(self.key)
        except OSError as e:
            print("{} file error {}".format(key_file_path, e.errno))

    def save_config(self, config_file_path, encrypted_config):

        """Save json configuration file

        Parameters
        ----------
        config_file_path : str
            Path to config file
        encrypted_config: bool
            Use encrypted configuration file
        """
        #
        data = None
        #
        if encrypted_config:
            fernet = Fernet(self.key)
            # encrypting the file
            data = fernet.encrypt(json.dumps(self.data, ensure_ascii=False).encode("utf-8"))
        else:
            data = json.dumps(self.data, ensure_ascii=False, indent=4).encode("utf-8")
        # opening the file in write mode and writing the encrypted data
        try:
            with open(config_file_path, "wb") as config_file:
                config_file.write(data)
        except OSError as e:
            print("{} file error {}".format(config_file_path, e.errno))

    def load_config(self):

        """Loads json configuration"""

        data = None
        try:
            with open(self.config_file_path, "rb") as config:
                c = config.read()
                data = json.loads(c)
                # print(json.dumps(data, indent=4))
        except OSError as e:
            print("{} file error {}".format(self.config_file_path, e.errno))
        #
        if self.encrypted_config:
            #
            fernet = Fernet(self.key)
            # decrypting the file
            try:
                self.data = json.loads(fernet.decrypt(data))
            except InvalidToken:
                print("Invalid Key - Unsuccessfully decrypted")
                sys.exit(1)
        else:
            self.data = data

    def new_config(self, config_file_path):
        """Generate New Config"""

        if "PYTEST_CURRENT_TEST" in os.environ:
            if "MAIL_USER" not in os.environ:
                print("MAIL_USER is unset")
                sys.exit(1)
            if "MAIL_PASSWORD" not in os.environ:
                print("MAIL_PASSWORD is unset")
                sys.exit(1)
            if "MAIL_SERVER" not in os.environ:
                print("MAIL_SERVER is unset")
                sys.exit(1)
            if "MAIL_PORT" not in os.environ:
                print("MAIL_PORT is unset")
                sys.exit(1)
            if "MAIL_SECURITY" not in os.environ:
                print("MAIL_SECURITY is unset")
                sys.exit(1)
        else:
            if "MAIL_USER" not in os.environ:
                os.environ["MAIL_USER"] = input("mail User: ")
            if "MAIL_PASSWORD" not in os.environ:
                os.environ["MAIL_PASSWORD"] = stdiomask.getpass("mail Password: ")
            if "MAIL_SERVER" not in os.environ:
                os.environ["MAIL_SERVER"] = input("mail Server: ")
            if "MAIL_PORT" not in os.environ:
                os.environ["MAIL_PORT"] = input("mail Port: ")
            if "MAIL_SECURITY" not in os.environ:
                os.environ["MAIL_SECURITY"] = input("mail Security: ")
        #
        self.data = {
            "compose": {},
            "email": {
                "active_auth": 0,
                "active_content": 0,
                "rotate_auth": "FALSE",
                "rotate_content": "FALSE",
                "auth": [
                    {
                        "user": os.environ["MAIL_USER"],
                        "password": os.environ["MAIL_PASSWORD"],
                        "port": os.environ["MAIL_PORT"],
                        "sender": os.environ["MAIL_USER"],
                        "server": os.environ["MAIL_SERVER"],
                        "security": os.environ["MAIL_SECURITY"],
                    }
                ],
                "content": [{"markdown": "neurorights.md", "subject": ""}],
            },
            "scrape": {
                "use_tor": "FALSE",
                "use_proxies": "FALSE",
                "proxies": {
                    "http": "http://10.10.1.10:3128",
                    "https": "http://10.10.1.10:1080",
                },
                "invalid_domains": [
                    "adobe.",
                    "aerialtelly.",
                    "allmovie",
                    "altavista.",
                    "amazon.",
                    "aol.",
                    "apache.",
                    "apple.",
                    "ask.",
                    "bing.",
                    "creativecommons.",
                    "debian.",
                    "dmoz.",
                    "domaintools.",
                    "duckduckgo.",
                    "ecosia.",
                    "facebook.",
                    "github.",
                    "google.",
                    "imdb.",
                    "justgiving.",
                    "microsoft.",
                    "movieinsider.",
                    "mozilla.",
                    "musicmoz.",
                    "oracle.",
                    "patreon.",
                    "phpbb.",
                    "reddit.",
                    "rottentomatoes.",
                    "startpage.",
                    "symfony.",
                    "w3.",
                    "wikipedia.",
                    "wikimedia.",
                    "windows.",
                    "wordpress.",
                    "xmlmind.",
                    "yahoo.",
                    "yandex.",
                    "yelp.",
                    "youtube.",
                ],
                "invalid_files": [
                    ".pdf",
                    ".iso",
                    ".gz",
                    ".bz2",
                    ".tar",
                    ".zip",
                    ".jpg",
                    ".jpeg",
                    ".mp3",
                    ".mp4",
                    ".png",
                    ".svg",
                    ".gif",
                    ".webp",
                    ".yji",
                    ".css",
                    ".js",
                ],
                "invalid_paths": ["forum", "admin", "auth"],
                "targets": {
                    "activism": "https://curlie.org/en/Society/Activism",
                    "addiction": "https://curlie.org/en/Health/Addictions/",
                    "defense": "https://curlie.org/en/Business/Aerospace_and_Defense/Defense/",
                    "education": "https://curlie.org/en/Reference/Education",
                    "embassies": "https://curlie.org/en/Society/Government/Embassies_and_Consulates/By_Country_of_Origin",
                    "islam": "https://curlie.org/en/Society/Religion_and_Spirituality/Islam/",
                    "journalists": "https://curlie.org/en/News/Journalism/",
                    "museums": "https://curlie.org/en/Reference/Museums/Arts_and_Entertainment/Art_Museums",
                    "music": "https://curlie.org/en/Arts/Music/Bands_and_Artists/",
                    "religion": "https://curlie.org/en/Society/Religion_and_Spirituality/",
                    "rescue": "https://curlie.org/Society/Religion_and_Spirituality/Christianity/Organizations/Rescue/",
                    "ukraine": "https://curlie.org/en/Regional/Europe/Ukraine/",
                },
            },
            "social": {
                "facebook": {"access_token": "", "page_id": ""},
                "twitter": {
                    "access_token": "",
                    "access_token_secret": "",
                    "consumer_key": "",
                    "consumer_secret": "",
                    "handles": [
                        "@UNPOL @UNODC @WHO @Cyber_Torture @theintercept",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                        "",
                    ],
                },
            },
        }
        #
        self.save_config(config_file_path, self.encrypted_config)
