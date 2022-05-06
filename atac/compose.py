from .config import Config
from .art import *
from .epicycle_drawing import *
from .paraphrase import *
from .util import trace

# custom latex rendere
from .MisTeX.Renderer import Renderer
# Always use this if you want raw latex beyond simple $ and $$
# anywhere in the input
from .MisTeX.Escape import escape

from datetime import datetime
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import mistune
import regex

#from html2image import Html2Image

from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

from googletrans import Translator
import language_tool_python


class AllTimeHigh(Config):
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
    generate_key()
        Generates a new encryption key from a password + salt
    """

    @staticmethod
    def fix_mixed_encoding(s):
        """ Fixed mixed encoding

        Parameters
        ----------
        s : str
            The mixed encoding string to fix
        """
        output = ''
        ii = 0
        for _ in s:
            if ii <= len(s)-1:
                if s[ii] == '\\' and s[ii+1] == 'x':
                    b = s[ii:ii+4].encode('ascii').decode('utf-8')
                    output = output+b
                    ii += 3
                else:
                    output = output+s[ii]
            ii += 1
        #
        return output


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
        #spellchecker = language_tool_python.LanguageToolPublicAPI(translate_to_languagecode if translate_to_languagecode else 'en')
        #
        subject_transform = "neurorights and blue whale suicide games: {}".format(subject.lower())
        if translate_to_languagecode:
            subject_translator = Translator()
            subject_transform = subject_translator.translate(text=subject_transform, dest=translate_to_languagecode).text
        elif do_paraphrase:
            nlp = spacy.load('en_core_web_md')
            subject_transform = get_paraphrase(subject_transform, nlp)
        # clean html
        # subject_transform = BeautifulSoup(subject_transform, features="lxml").get_text()
        # check spelling
        # spellchecker_subject_matches = spellchecker.check(subject_transform)
        # is_bad_subject_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
        # spellchecker_subject_matches = [rule for rule in spellchecker_subject_matches if not is_bad_subject_rule(rule)]
        # subject_transform = language_tool_python.utils.correct(subject_transform, spellchecker_subject_matches)
        #
        message["Subject"] = "{} - AMYTAL - {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), subject_transform.capitalize())
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        lines = []
        for phrase in message_content:
            phrase_transform = phrase
            if phrase_transform.find("<img src=") != -1:
                lines.append(phrase_transform)
                print("Found image")
                continue
            if phrase_transform.find("$$") != -1:
                lines.append(phrase_transform.strip())
                print("Found latex")
                continue
            if not phrase_transform:
                print("Found empty line")
                lines.append("")
                continue
            # translation transform
            if translate_to_languagecode:
                print("translating phrase to {}...".format(translate_to_languagecode))
                phrase_translator = Translator()
                print("before translation: " + phrase_transform)
                phrase_transform = phrase_translator.translate(text=phrase_transform.lower(), dest=translate_to_languagecode).text
                print("after translation: " + phrase_transform)
            # paraphrasing transform
            elif do_paraphrase: 
                phrase_transform = get_paraphrase(phrase_transform.lower(), nlp)
            # remove html
            # phrase_transform = BeautifulSoup(phrase_transform, features="lxml").get_text()
            # check spelling
            # spellchecker_matches = spellchecker.check(phrase_transform)
            # is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
            # spellchecker_matches = [rule for rule in spellchecker_matches if not is_bad_rule(rule)]
            # phrase_transform = language_tool_python.utils.correct(phrase_transform, spellchecker_matches)
            phrase_transform = phrase_transform.capitalize()
            lines.append(phrase_transform)
        #
        message_str = "\n".join(lines)
        print("message: "+json.dumps(message_str, indent=4))
        message_soup = BeautifulSoup(message_str, 'lxml')
        text = regex.sub(r'\n\n\n+', '\n\n', message_soup.get_text().strip())
        #
        # Create parser
        #markdown = mistune.create_markdown(renderer=Renderer(), plugins=[escape])

        # the end of sub class
        #html to LaTex
        # render the markdown into HTML 
        # headers_css = "<link rel='stylesheet' href='https://cdnjs.cloudflaregex.com/ajax/libs/materialize/1.0.0/css/materialize.min.css'>"
        # headers_js = "<script src='https://cdnjs.cloudflaregex.com/ajax/libs/materialize/1.0.0/js/materialize.min.js></script>"
        html_header = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='utf-8'>
            <meta name='viewport' content='width=device-width'>
            <title>MathJax example</title>
            <style type="text/css">
                p {margin:25px 77px;}
                ol {margin:25px 77px;}
                ul {margin:25px 77px;}
                li p {margin:5px;}
            </style>
            <script src='https://polyfill.io/v3/polyfill.min.js?features=es6'></script>
            <script id='MathJax-script' async src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'></script>
        </head>
        </body>
        """
        #html_content = "<p align='center' width='100%'><img src='cid:header'></p>" + mistune.html(message_str) + "<p align='center' width='100%'><img src='cid:signature'></p>"
        html_footer = "</body></html>"
        html = html_header + mistune.html(message_str) + html_footer
        # Turn these into plain/html MIMEText objects
        part1 = MIMENonMultipart('text', 'plain', charset='utf-8')
        part2 = MIMENonMultipart('text', 'html', charset='utf-8')
        part1.set_payload(text, charset=cs)
        part2.set_payload(html, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(part1)
        body.attach(part2)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        #
        '''
        hfp = open('data/messages/assets/img/jesus/jesus_king.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        
        hti = Html2Image()
        hti.screenshot(mistune.html(message_str), save_as='content.png')
        cfp = open('content.png', 'rb')
        msg_image_content = MIMEImage(cfp.read())
        cfp.close()
        # Define the image's ID as referenced above
        msg_image_content.add_header('Content-ID', '<content>')
        message.attach(msg_image_content)
        
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
