"""
Create portable serialized representations of Python objects.
See module copyreg for a mechanism for registering custom picklers.
See module pickletools source for extensive comments.

Classes:

    Pickler
    Unpickler

Functions:

    dump(object, file)
    dumps(object) -> string
    load(file) -> object
    loads(string) -> object

Misc variables:

    __version__
    format_version
    compatible_formats
"""

from .Config import Config
from .Compose import Compose
from .Clean import Clean
from .Scrape import Scrape
#
from .send.Email import SendEmail
from .send.Chat import SendChat
from .send.IRC import SendIRC
from .send.Social import SendSocial
from .Util import *

__all__ = ['Config', 'Compose', 'Clean', 'Scrape', 'SendChat', 'SendEmail', 'SendIRC', 'SendSocial', 'Util']
