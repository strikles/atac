from ..config.Config import Config

import os
import csv
from tqdm import tqdm

import validators
from validators import ValidationFailure

import phonenumbers
from phonenumbers import NumberParseException, phonenumberutil


class Clean(Config):
    """
    A class used to represent a Configuration object

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

    @staticmethod
    def clean_phones(path):
        """
        Generate New Config

        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        num_legs : int, optional
            The number of legs the animal (default is 4)
        """
        print(path)
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith(".csv"), os.listdir(path)))
        for ml in ml_files:
            cf = path + ml
            print(cf)
            # read
            with open(cf) as file:
                lines = file.readlines()
                with tqdm(total=len(lines)) as progress:
                    for _, phone in csv.reader(lines):
                        print(phone)
                        try:
                            z = phonenumbers.parse(phone)
                            valid_number = phonenumbers.is_valid_number(z)
                            if valid_number:
                                line_type = phonenumberutil.number_type(z)
                                print(line_type)
                        except NumberParseException as e:
                            print(str(e))

    @staticmethod
    def clean_emails(path):
        """
        Generate New Config

        Parameters
        ----------
        name : str
            The name of the animal
        sound : str
            The sound the animal makes
        num_legs : int, optional
            The number of legs the animal (default is 4)
        """
        print(path)
        # get mailing list csv files
        ml_files = list(filter(lambda c: c.endswith(".csv"), os.listdir(path)))
        for ml in ml_files:
            cf = path + ml
            print(cf)
            ml_emails = []
            # read
            with open(cf) as file:
                lines = file.readlines()
                with tqdm(total=len(lines)) as progress:
                    for ndx, receiver_email in csv.reader(lines):
                        if validators.email(receiver_email):
                            ml_emails.append({"index": ndx, "email": receiver_email})
                        else:
                            print("{0} INVALID".format(receiver_email))
                        progress.update(1)
            # write
            with open(cf, mode="a") as file2:
                file2.truncate(0)
                with tqdm(total=len(ml_emails)) as progress2:
                    writer = csv.writer(
                        file2, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )
                    writer.writerow(["", "email"])
                    for item in ml_emails:
                        writer.writerow([item["index"], item["email"]])
                        progress2.update(1)
