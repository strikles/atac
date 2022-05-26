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

from .config.Config import Config

from .art.Art import Art
from .compose.Compose import Compose
from .send.Clean import Clean
from .scrape.Scrape import Scrape

#
from .send.Email import SendEmail
from .send.Chat import SendChat
from .send.IRC import SendIRC
from .send.Social import SendSocial

__all__ = [
    "Config",
    "Art",
    "Compose",
    "Clean",
    "Scrape",
    "SendChat",
    "SendEmail",
    "SendIRC",
    "SendSocial"
]
