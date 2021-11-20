import os
import sys
#import json
#import yaml
import markdown
import markovify
import qrcode
import ascii_magic

from email import charset
#from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from .config import Config


class AllTimeHigh(Config):

    def __init__(self, encrypted_config=True, config_file_path='auth.json', key_file_path=None):
        """ class init

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
    def generate_ascii(image_path):
        '''
        '''
        if not os.path.isfile(image_path):
            print("Invalid image path!")
            sys.exit(1)
        #
        art = ascii_magic.from_image_file(
            img_path=image_path,
            columns=200,
            mode=ascii_magic.Modes.HTML
        )
        #
        ascii_magic.to_html_file('ascii.html', art, additional_styles='background: #222;')
        return art

    @staticmethod
    def generate_markov_content(content):
        '''
        '''
        # Build the model.
        text_model = markovify.Text(content, state_size=3)
        # return randomly-generated sentence of no more than 280 characters
        return text_model.make_short_sentence(200)

    @staticmethod
    def fix_mixed_encoding(s):
        '''
        '''
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

    def compose_encrypted_email(self, sender_email, recipient_email, key_id, message_content, subject):
        '''
        '''
        message = MIMEMultipart("mixed")
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        message.replace_header('format', 'flowed')
        #
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipient_email
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        body.replace_header('format', 'flowed')
        # convert markdown to html
        text = message_content
        html = markdown.markdown(text)
        # Encrypt the message body.
        encrypted_text = self.gpg.encrypt(text, key_id)
        encrypted_html = self.gpg.encrypt(html, key_id)
        # Turn these into plain/html MIMEText objects
        part1 = MIMENonMultipart('text', 'plain', charset='utf-8')
        part2 = MIMENonMultipart('text', 'html', charset='utf-8')
        part1.set_payload(encrypted_text, charset=cs)
        part2.set_payload(encrypted_html, charset=cs)
        # Add HTML/plain-text parts to MIMEMultipart message
        body.attach(part1)
        body.attach(part2)
        # The email client will try to render the last part first
        message.attach(body)
        print(message.as_string())
        #
        return message

    @staticmethod
    def compose_email(sender_email, mailing_list, message_content, subject):
        '''
        '''
        message = MIMEMultipart("mixed")
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        text = message_content
        html = markdown.markdown(text)
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
        return message

    @staticmethod
    def create_image(text, window_height, window_width):
        '''
        '''
        img = Image.new('L', (window_height, window_width), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial", 24)
        draw.text((0, 0), text, font=font)
        img.save('content.jpg')

    @staticmethod
    def create_qr_code(url):
        '''
        '''
        # instantiate QRCode object
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        # add data to the QR code
        qr.add_data(url)
        # compile the data into a QR code array
        qr.make()
        # print the image shape
        # print("The shape of the QR image:", np.array(qr.get_matrix()).shape)
        # transfer the array into an actual image
        img = qr.make_image(fill_color="white", back_color="black")
        # save it to a file
        img.save("qr.png")
