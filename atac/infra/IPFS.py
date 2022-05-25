import ipfshttpclient

from .util.Util import *
from .config.Config import Config


class IPFS(Config):

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
    """

    """
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
        self._client = ipfshttpclient.connect(session=True)

    def upload_directory_to_ipfs(self, art_directory_path):
        # Share TCP connections using a context manager
        self._client.add(art_directory_path, recursive=True)
        print(self._client.stat(hash))
        return hash

    def upload_files_in_directory_to_ipfs(self, art_directory, file_pattern):
        self._client.add(art_directory, pattern=file_pattern)
        return hash

    # Call this when your done
    def close_ipfs(self):
        self._client.close()
