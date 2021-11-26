from .config import Config

import ascii_magic
from datetime import datetime
from email import charset
#from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart
from email.mime.nonmultipart import MIMENonMultipart

from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np

import markdown
import markovify
import math
import os
import qrcode
import random
from samila import GenerativeImage
import sys

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


class AllTimeHigh(Config):
    """
    A class used to represent a Configuration object

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
    generate_key()
        Generates a new encryption key from a password + salt
    """

    @staticmethod
    def generate_ascii(image_path):
        """
        Generate New Config

        Parameters
        ----------
        image_path : str
            Path to image file
        """
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
        """
        Generate Markov Content

        Parameters
        ----------
        content : str
            Corpus to generate markov sequences from
        """
        # Build the model.
        text_model = markovify.Text(content, state_size=3)
        # return randomly-generated sentence of no more than 280 characters
        return text_model.make_short_sentence(200)

    @staticmethod
    def fix_mixed_encoding(s):
        """
        Fixed mixed encoding

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
        """
        Return datetime string

        """
        # datetime object containing current date and time
        now = datetime.now()
        # print("now =", now)
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)
        #
        return dt_string

    def compose_encrypted_email(self, sender_email, recipient_email, key_id, message_content, subject):
        """
        Compose MIMEMultipart encrypted email message

        Parameters
        ----------
        sender_email : str
            The name of the animal
        recipient_email: str
            The sound the animal makes
        key_id : int, optional
            The gnupg keyid for the email addresses
        message_content : str
            The message to send
        subject : str
            The message subject
        """
        message = MIMEMultipart("mixed")
        cs = charset.Charset('utf-8')
        cs.header_encoding = charset.QP
        cs.body_encoding = charset.QP
        message.set_charset(cs)
        message.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        message.replace_header('format', 'flowed')
        #
        message["Subject"] = self.get_datetime() + " " + subject
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
        """
        Compose MIMEMultipart email message

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

    def generate_art_samila(self):
        """
        """
        def f1(x,y):
            result = random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)
            return result
        def f2(x,y):
            result = random.uniform(-1,1) * y**3 - math.cos(x**2) + 2*x
            return result
        #
        g = GenerativeImage(f1,f2)
        g.generate()
        #g.plot()
        g.save_image(file_adr="samila.png")

    @staticmethod
    def create_image(text, window_height, window_width):
        """
        Generate Image from text

        Parameters
        ----------
        text : str
            The name of the animal
        window_height : int
            The image height
        window_width : int
        The image width
        """
        img = Image.new('L', (window_height, window_width), color='white')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial", 24)
        draw.text((0, 0), text, font=font)
        img.save('content.jpg')

    @staticmethod
    def create_qr_code(url):
        """
        Generate QR Code

        Parameters
        ----------
        url : str
            The QR code data
        """
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

class Fractal:
    """
    """
    @staticmethod
    def mandelbrot(z, max_iter):
        c = z
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    @staticmethod
    def mandelbrot_set(x_min, x_max, y_min, y_max, width, height, max_iter):
        r1 = np.linspace(x_min, x_max, width)
        r2 = np.linspace(y_min, y_max, height)
        n3 = np.empty((width, height))
        for i in range(width):
            for j in range(height):
                n3[i,j] = self.mandelbrot(r1[i] + 1j*r2[j], max_iter)
        return (r1, r2, n3)

    @staticmethod
    def mandelbrot_image(x_min, x_max, y_min, y_max, width=10, height=10, max_iter=80, cmap='hot'):
        dpi = 72
        img_width = dpi * width
        img_height = dpi * height
        x, y, z = self.mandelbrot_set(x_min, x_max, y_min, y_max, img_width, img_height, max_iter)
        #
        fig, ax = plt.subplots(figsize=(width, height), dpi=72)
        ticks = np.arange(0, img_width, 3*dpi)
        x_ticks = x_min + (x_max - x_min)*ticks/img_width
        plt.xticks(ticks, x_ticks)
        y_ticks = y_min + (y_max - y_min)*ticks/img_width
        plt.yticks(ticks, y_ticks)
        #
        plt.axis('off')
        norm = colors.PowerNorm(0.3)
        ax.imshow(z.T, cmap=cmap, origin='lower')
        plt.show()
        self.save_image(fig)

    @staticmethod
    def save_image(fig):
        filename = "mandelbrot.png"
        fig.savefig(filename)
        self.mandelbrot_image(-2.0, 0.5, -1.25, 1.25, cmap='viridis')

class Invader:
    """
    """
    origDimension = 1500

    r = lambda: random.randint(50,255)
    rc = lambda: ('#%02X%02X%02X' % (r(),r(),r()))
    listSym = []
    #
    @staticmethod
    def create_square(border, draw, randColor, element, size):
        if (element == int(size/2)):
            draw.rectangle(border, randColor)
        elif (len(listSym) == element+1):
            draw.rectangle(border,listSym.pop())
        else:
            listSym.append(randColor)
            draw.rectangle(border, randColor)

    @staticmethod
    def create_invader(border, draw, size):
        x0, y0, x1, y1 = border
        squareSize = (x1-x0)/size
        randColors = [rc(), rc(), rc(), (0,0,0), (0,0,0), (0,0,0)]
        incrementer = 1
        element = 0
        #
        for y in range(0, size):
            incrementer *= -1
            element = 0
            for x in range(0, size):
                topLeftX = x*squareSize + x0
                topLeftY = y*squareSize + y0
                botRightX = topLeftX + squareSize
                botRightY = topLeftY + squareSize
                #
                self.create_square((topLeftX, topLeftY, botRightX, botRightY), draw, random.choice(randColors), element, size)
                if (element == int(size/2) or element == 0):
                    incrementer *= -1;
                element += incrementer

    @staticmethod
    def run(size, invaders, imgSize):
        #
        origDimension = imgSize
        origImage = Image.new('RGB', (origDimension, origDimension))
        draw = ImageDraw.Draw(origImage)
        #
        invaderSize = origDimension/invaders
        print(invaderSize)
        padding = invaderSize/size
        print(padding)
        # Will eventually create many
        finalBotRightX = 0
        finalBotRightY = 0
        for x in range(0, invaders):
            for y in range(0, invaders):
                topLeftX = x*invaderSize + padding
                topLeftY = y*invaderSize + padding
                botRightX = topLeftX + invaderSize - padding*2
                botRightY = topLeftY + invaderSize - padding*2

                finalBotRightX = botRightX
                finalBotRightY = botRightY
                self.create_invader((topLeftX, topLeftY, botRightX, botRightY), draw, size)
        #    origImage.save("Examples/Example-"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")
        origImage.crop((0, 0, botRightX-padding, botRightY-padding)).save("Examples/paddingTest.jpg")
