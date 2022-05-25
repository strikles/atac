from ..compose.Compose import Compose
from ..util.Util import trace

from envelope import Envelope
import os
import random
import sys


class Send(Compose):
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
    """

    def __init__(
        self, encrypted_config=True, config_file_path="auth.json", key_file_path=None
    ):
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
        super().__init__(encrypted_config, config_file_path, key_file_path)

    def get_contact_files(self, contact_files_path):
        """Get contact files

        Parameters
        ----------
        contact_files_path : str
            The path to the contacts CSV
        """
        contact_files = None
        #
        if os.path.isdir(contact_files_path):
            contact_files = list(
                map(
                    trace(lambda p: os.path.join(contact_files_path, p)),
                    list(
                        filter(
                            lambda c: c.endswith(".csv"), os.listdir(contact_files_path)
                        )
                    ),
                )
            )
            random.shuffle(contact_files)
        elif os.path.isfile(contact_files_path):
            contact_files = [contact_files_path]
        else:
            print("Invalid contact file path!")
            sys.exit(1)
        #
        return contact_files

    def send_batch(
        self,
        email_files_path,
        message_file_path,
        subject,
        do_paraphrase,
        translate_to_languagecode,
    ):
        pass

    def send(
        self,
        mailing_list,
        message_content,
        subject,
        do_paraphrase,
        translate_to_languagecode=None,
    ):
        pass
