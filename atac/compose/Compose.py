from ctypes.wintypes import LANGID
from ..config.Config import Config

#from .art import *
#from .art.epicycles import *
from .Translate import *
from .Paraphrase import *
from .Latex import *
from ..util.Util import trace
#
from datetime import datetime
#
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
#
import json
import mistune
import pystache
import regex

import uuid

#from html2image import Html2Image

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


from autocorrect import Speller

class Compose(Config):
    """ A class used to represent a Configuration object

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

    @staticmethod
    def mjml2html(content):
        # Create parser
        # markdown = mistune.create_markdown(renderer=Renderer(), plugins=[escape])
        # read in the email template, remember to use the compiled HTML version!
        email_template = ("\n".join(content))
        # Pass in values for the template using a dictionary
        template_params = {'first_name': 'JustJensen'}
        # Attach the message to the Multipart Email
        text_content = ""
        html_content = pystache.render(email_template, template_params)
        #
        return html_content

    @staticmethod
    def md2html(content, do_paraphrase, languagecode):
        #html_content = "<p align='center' width='100%'><img src='cid:header'></p>" + mistune.html(message_str) + "<p align='center' width='100%'><img src='cid:signature'></p>"
        html_header = """
        <!doctype html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style type="text/css">
                @font-face {
                    font-family: 'Timmana';
                    font-style: normal;
                    font-weight: 400;
                    src: local('Timmana'), url(https://fonts.gstatic.com/s/timmana/v3/6xKvdShfL9yK-rvpOmzRKV4KQOI.woff2) format('woff2');
                }
                body {
                    background-color: #FFF;
                    list-style: lower-greek inside;
                    line-height: 3;
                    opacity: 1;
                    text-align: left;
                    transition: opacity 1s ease 0s;
                    word-spacing: 3px;
                }
                p {
                    margin: 25px 77px;
                }
                li > p {
                    margin: auto 10px;
                }
                img {
                    opacity: 0.7;
                }
                img:hover {
                    opacity: 1;
                }
                td {
                    padding-top: 10px;
                    padding-bottom: 10px;
                }
            </style>
        </head>
        <body>
        """
        html_footer = "</body></html>"
        lines = Compose.transform(content, do_paraphrase, languagecode)
        # render the markdown into HTML
        message_str = "\n".join(lines)
        print("message: "+json.dumps(message_str, indent=4))
        html_content = html_header + mistune.html(message_str) + html_footer
        #
        return html_content


    @staticmethod
    def transform(content, do_paraphrase, src='en', dest=None):
        #
        lines = []
        num_latex_lines = 0
        for phrase in content:
            #
            phrase_transform = phrase
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
            # translation
            if dest:
                phrase_transform = Compose.spellcheck(phrase_transform, src)
                phrase_transform = Compose.translate(phrase_transform, src, dest)
                phrase_transform = Compose.spellcheck(phrase_transform, dest)
            # paraphrasing transform
            elif do_paraphrase:
                phrase_transform = Compose.spellcheck(phrase_transform, src)
                phrase_transform = Compose.paraphrase(phrase_transform, src, dest)
                phrase_transform = Compose.spellcheck(phrase_transform, dest)
            #
            phrase_transform = phrase_transform.capitalize()
            lines.append(phrase_transform)
        #
        return lines


    @staticmethod
    def compose_email(sender_email, mailing_list, message_content, subject, do_paraphrase, translate_to_languagecode=None):

        """ Compose MIMEMultipart email message

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
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        nlp = None
        subject_prefix = "{} - AMYTAL - neurorights, blue whale suicide games and tongue articulators".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        subject_content = []
        subject_content.append(subject.lower())
        subject_transform = Compose.transform(subject_content, do_paraphrase, translate_to_languagecode)
        #
        message["Subject"] = "{0}: {1}".format(subject_prefix, subject_transform)
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        message_type = "markdown"
        html_content = ""
        if message_type == "html":
            html_content = "\n".join(message_content)
        elif message_type == "mjml":
            html_content = Compose.mjml2html(message_content, do_paraphrase, translate_to_languagecode)
        elif message_type == "markdown":
            html_content = Compose.md2html(message_content, do_paraphrase, translate_to_languagecode)
        # get text
        text_soup = BeautifulSoup(html_content, 'lxml')
        text_content = regex.sub(r'\n\n\n+', '\n\n', text_soup.get_text().strip())
        # set text payload
        text_part = MIMENonMultipart('text', 'plain', charset='utf-8')
        text_part.set_payload(text_content, charset=cs)
        # set html payload
        html_part = MIMENonMultipart('text', 'html', charset='utf-8')
        html_part.set_payload(html_content, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(text_part)
        body.attach(html_part)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        '''
        #
        sfp = open('data/messages/assets/img/jesus/mary.png', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        '''
        #
        return message
