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
#
import latex2mathml.converter
from .latex2svg import latex2svg
import pylatexenc
from pylatexenc.latex2text import LatexNodes2Text
#
import pystache

from datetime import datetime
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import mistune
import regex
from sympy import preview

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
        #
        subject_transform = "neurorights and blue whale suicide games: {}".format(subject.lower())
        if translate_to_languagecode:
            subject_translator = Translator()
            subject_transform = subject_translator.translate(text=subject_transform, dest=translate_to_languagecode).text
        elif do_paraphrase:
            nlp = spacy.load('en_core_web_md')
            subject_transform = get_paraphrase(subject_transform, nlp)
        #
        if False:
            subject_transform = BeautifulSoup(subject_transform, features="lxml").get_text()
            # check spelling
            spellchecker_subject_matches = spellchecker.check(subject_transform)
            is_bad_subject_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
            spellchecker_subject_matches = [rule for rule in spellchecker_subject_matches if not is_bad_subject_rule(rule)]
            subject_transform = language_tool_python.utils.correct(subject_transform, spellchecker_subject_matches)
        #
        message["Subject"] = "{} - AMYTAL - {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), subject_transform.capitalize())
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        message_type = "markdown"
        html_content = ""
        #
        if message_type == "mjml":
            # Create parser
            # markdown = mistune.create_markdown(renderer=Renderer(), plugins=[escape])
            # read in the email template, remember to use the compiled HTML version!
            email_template = ("\n".join(message_content))
            # Pass in values for the template using a dictionary
            template_params = {'first_name': 'JustJensen'}
            # Attach the message to the Multipart Email
            html_content = pystache.render(email_template, template_params)
        else:
            lines = []
            num_latex_lines = 0
            for phrase in message_content:
                phrase_transform = phrase
                # images
                if phrase_transform.find("<img src=") != -1:
                    print("Found image")
                    lines.append(phrase_transform)
                    continue
                # LaTeX
                if phrase_transform.startswith("$$") and phrase_transform.endswith("$$"):
                    print("Found latex {}".format(phrase_transform))
                    phrase_transform = phrase_transform.replace("$$", "")    
                    '''
                    # generate image
                    latex_image_file = 'data/messages/assets/latex{}.png'.format(num_latex_lines)
                    if not os.path.isfile(latex_image_file):
                        preview(phrase_transform, viewer='file', filename=latex_image_file, euler=False)
                    else:
                        lines.append("<p align='center' width='100%'><img src='https://raw.githubusercontent.com/strikles/atac-data/main/messages/assets/latex{}.png'></p>".format(num_latex_lines))   
                    '''
                    # mathml
                    # phrase_transform = latex2mathml.converter.convert(phrase_transform)
                    # print("transformed latex {}".format(phrase_transform))
                    #
                    # ascii
                    # phrase_transform = LatexNodes2Text().latex_to_text(phrase_transform)
                    # print("transformed latex {}".format(phrase_transform))
                    #
                    # svg
                    # phrase_transform = latex2svg(phrase_transform)['svg']
                    # print("transformed latex {}".format(phrase_transform))
                    #
                    lines.append(phrase_transform)
                    continue
                # empty line
                if not phrase_transform:
                    print("Found empty line")
                    lines.append("")
                    continue
                # translation
                if translate_to_languagecode:
                    print("translating phrase to {}...".format(translate_to_languagecode))
                    phrase_translator = Translator()
                    print("before translation: " + phrase_transform)
                    phrase_transform = phrase_translator.translate(text=phrase_transform.lower(), dest=translate_to_languagecode).text
                    print("after translation: " + phrase_transform)
                # paraphrasing transform
                elif do_paraphrase: 
                    phrase_transform = get_paraphrase(phrase_transform.lower(), nlp)
                #
                # check spelling
                if False:
                    spellchecker = language_tool_python.LanguageToolPublicAPI(translate_to_languagecode if translate_to_languagecode else 'en')
                    spellchecker_matches = spellchecker.check(phrase_transform)
                    is_bad_rule = lambda rule: rule.message == 'Possible spelling mistake found.' and len(rule.replacements) and rule.replacements[0][0].isupper()
                    spellchecker_matches = [rule for rule in spellchecker_matches if not is_bad_rule(rule)]
                    phrase_transform = language_tool_python.utils.correct(phrase_transform, spellchecker_matches)
                #
                phrase_transform = phrase_transform.capitalize()
                lines.append(phrase_transform)
            #
            # render the markdown into HTML
            message_str = "\n".join(lines)
            print("message: "+json.dumps(message_str, indent=4))
            #html_content = "<p align='center' width='100%'><img src='cid:header'></p>" + mistune.html(message_str) + "<p align='center' width='100%'><img src='cid:signature'></p>"
            html_content = mistune.html(message_str)
        #
        # text payload
        text_soup = BeautifulSoup(html_content, 'lxml')
        text_content = regex.sub(r'\n\n\n+', '\n\n', text_soup.get_text().strip())
        text_part = MIMENonMultipart('text', 'plain', charset='utf-8')
        text_part.set_payload(text_content, charset=cs)
        # html payload
        html_part = MIMENonMultipart('text', 'html', charset='utf-8')
        html_part.set_payload(html_content, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(text_part)
        body.attach(html_part)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        #
        '''
        #
        hfp = open('data/messages/assets/img/jesus/jesus_king.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        #
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
