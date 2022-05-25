from .Send import Send

import time


class SendSocial(Send):
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
        self.social = self.data["social"]
