from .art import *
from .epicycle_drawing import *
from .config import Config

from datetime import datetime
from email import charset
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart
import mistune
import os
import sys

from transformers import *

from bs4 import BeautifulSoup


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
    def get_datetime():
        """ Return datetime string

        """
        # datetime object containing current date and time
        now = datetime.now()
        # print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        #
        return dt_string

    @staticmethod
    def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
        # tokenize the text to be form of a list of token IDs
        inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
        # generate the paraphrased sentences
        outputs = model.generate(
            **inputs,
            num_beams=num_beams,
            num_return_sequences=num_return_sequences,
        )
        # decode the generated sentences using the tokenizer to get them back to text
        return tokenizer.batch_decode(outputs, skip_special_tokens=True)


    @staticmethod
    def compose_email(sender_email, mailing_list, message_content, subject, do_paraphrase):

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
        if not do_paraphrase:
            message["Subject"] = subject
        else:
            model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
            tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
            #tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")
            #model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")
            #
            message["Subject"] = AllTimeHigh.get_paraphrased_sentences(model, tokenizer, subject, num_beams=10, num_return_sequences=1)
        #
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        text = None
        if not do_paraphrase:
            text = message_content
        else:
            text = []
            for phrase in message_content:
                if bool(BeautifulSoup(phrase, "html.parser").find()):
                    text.append(phrase)
                else:
                    text.append(AllTimeHigh.get_paraphrased_sentences(model, tokenizer, subject, num_beams=10, num_return_sequences=1))
        #
        html = "<p align='center' width='100%'><img width='20%' src='cid:header'></p>" + mistune.html(text) + "<p align='center' width='100%'><img width='20%' src='cid:signature'></p>"
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
        hfp = open('data/assets/img/jesus/jesus_king.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        #
        sfp = open('data/assets/img/jesus/lamb_of_god.png', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        #
        return message
