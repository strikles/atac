from ctypes.wintypes import LANGID
from ..config.Config import Config
from ..util.Util import trace, get_file_content, fast_scandir
from ..art.Art import Art

# from .art import *
# from .art.epicycles import *
from .SpellCheck import spelling_corrector, correct_spelling_languagetool
from .Translate import translator
from .Paraphrase import paraphraser
from .Latex import *

#
from datetime import datetime
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
from glob import glob
import json
import mistune
import pystache
import os
import regex
import uuid

# from html2image import Html2Image

from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")


class Compose(Config):
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

    @staticmethod
    def mjml2html(content):
        # Create parser
        # markdown = mistune.create_markdown(renderer=Renderer(), plugins=[escape])
        # read in the email template, remember to use the compiled HTML version!
        email_template = "\n".join(content)
        # Pass in values for the template using a dictionary
        template_params = {"first_name": "JustJensen"}
        # Attach the message to the Multipart Email
        text_content = ""
        html_content = pystache.render(email_template, template_params)
        #
        return html_content

    @staticmethod
    def md2html(content):
        html_header = """
        <!doctype html>
        <html>
        <head>
            <meta name='viewport' content='width=device-width, initial-scale=1.0'>
            <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'>
            <style type='text/css'>

                @keyframes scaler {
                    from {
                        font-size: 1em;
                    }
                    to {
                        font-size: 1.2em;
                    }
                }

                body {
                    background-color: #FFF;
                    line-height: 3;
                    font-size: 1em;
                    opacity: 1;
                    text-align: left;
                    word-spacing: 3px;
                    transition: blur 1s ease-out, invert 1s ease-out, opacity 1s ease 0s;
                }

                svg {
                    display: none;
                }

                p {
                    margin: 25px 77px;
                    font-family: 'Yanone Kaffeesatz', sans-serif;
                }

                li {
                    margin: 7px 77px;
                    list-style: lower-greek inside;
                }

                li > p {
                    margin: auto 7px;
                }

                img.person {
                    opacity: 0.5;
                    margin: 7px 7px;
                    height:auto;
                    max-width: 100%;
                    filter: invert(100%);
                }

                img.person:hover {
                    opacity: 1;
                    filter: none;
                }

                td {
                    padding-top: 10px;
                    padding-bottom: 10px;
                }

                @media only screen and (max-width: 480px){

                    p {
                        margin: 25px 7px !important;
                        font-size: 1.2em;
                        font-family: 'Dosis', sans-serif;
                    }

                    img.person {
                        height:auto !important;
                        width: 100% !important;
                    }
                }
            </style>
        </head>
        <body>
            <svg>
                <defs>
                    <filter id="redOpacity" color-interpolation-filters='sRGB' x='0' y='0'>
                    <feColorMatrix type='matrix'
                            values='.50  0  0   0   0.50
                                    0.95 0  0   0   0.05
                                    0.95 0  0   0   0.05
                                    0    0  0   1   0' />
                    </filter>
                </defs>
            </svg>
        """
        html_footer = "</body></html>"
        lines = Compose.transform(content, False, False, False, False, False)
        # render the markdown into HTML
        message_str = "\n".join(lines)
        print("message: " + json.dumps(message_str, indent=4))
        html_content = html_header + mistune.html(message_str) + html_footer
        #
        return html_content

    @staticmethod
    def transform(
        content,
        paraphrase=False,
        translate=False,
        spellcheck=False,
        src="en",
        dest=False,
    ):
        #
        lines = []
        num_latex_lines = 0
        for phrase in content:
            #
            phrase_transform = phrase
            """
            if phrase_transform != mistune.html(phrase_transform):
                print("Found markup")
                lines.append(phrase_transform)
                continue
            """
            # images
            if phrase_transform.find("<img src=") != -1:
                print("Found image")
                lines.append(phrase_transform)
                continue
            # LaTeX
            if phrase_transform.startswith("$") and phrase_transform.endswith("$"):
                print("Found latex {}".format(phrase_transform))
                lines.append(phrase_transform)
                continue
            # empty line
            if not phrase_transform:
                print("Found empty line")
                lines.append("")
                continue
            # spellchecker
            if spellcheck:
                phrase_transform = spelling_corrector(phrase_transform, src)
            # translation
            if translate:
                phrase_transform = translator(phrase_transform, src, dest)
                if spellcheck:
                    phrase_transform = spelling_corrector(phrase_transform, dest)
            # paraphrasing transform
            if paraphrase:
                phrase_transform = paraphraser(phrase_transform, src)
                if spellcheck:
                    phrase_transform = spelling_corrector(phrase_transform, src)
            #
            phrase_transform = phrase_transform.capitalize()
            lines.append(phrase_transform)
        #
        return lines

    @staticmethod
    def compose_email(
        sender_email,
        mailing_list,
        message_content,
        subject,
        paraphrase,
        translate,
        correct_spelling,
        src="en",
        dest=False,
    ):

        """Compose MIMEMultipart email message

        Parameters
        ----------
        sender_email : str
            The name of the animal
        mailing_list : list
            The sound the animal makes
        message_content : str
            The message content to send
        subject : str
            The email subject
        """
        message = MIMEMultipart("mixed")
        cs = charset.Charset("utf-8")
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header("Content-Transfer-Encoding", "quoted-printable")
        #
        nlp = None
        subject_prefix = "{} - ".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        # "AMYTAL - Neurorights - Emile Barkhof and Jasper Kums act in criminal association with the CM93 Colegio Militar (largo da Luz, Portugal) group who abused me as a child and created the blue whale suicide game in 1993 abusing biophotonics instead of social media to issue tasks".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        subject_transform = Compose.transform(
            [subject], paraphrase, translate, correct_spelling, src, dest
        )
        #
        message["Subject"] = "{0}: {1}".format(
            subject_prefix, "".join(subject_transform)
        )
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header("Content-Transfer-Encoding", "quoted-printable")
        #
        message_type = "markdown"
        html_content = ""
        if message_type == "html":
            html_content = "\n".join(message_content)
        elif message_type == "mjml":
            html_content = Compose.mjml2html(message_content)
        elif message_type == "markdown":
            html_content = Compose.md2html(message_content)
        # get text
        text_soup = BeautifulSoup(html_content, "lxml")
        text_content = regex.sub(r"\n\n\n+", "\n\n", text_soup.get_text().strip())
        # set text payload
        text_part = MIMENonMultipart("text", "plain", charset="utf-8")
        text_part.set_payload(text_content, charset=cs)
        # set html payload
        html_part = MIMENonMultipart("text", "html", charset="utf-8")
        html_part.set_payload(html_content, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(text_part)
        body.attach(html_part)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        """
        sfp = open('data/messages/assets/img/jesus/mary.png', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        """
        #
        return message
