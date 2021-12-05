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

    def compose_encrypted_email(self, sender_email, recipient_email, key_id, message_content, subject):
        """ Compose MIMEMultipart encrypted email message

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
        html = mistune.html(text) + "<br><img src='cid:art'><br>"
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
        generate_art_samila()
        #
        #signature = Invader()
        #signature.run(17, 15, 427)
        #
        #sudoku = Sudoku()
        #sudoku.create()
        #sudoku.solve()
        #
        #gol = Conway()
        #gol.draw(427)
        #
        # This is just a simple box drawn in paint.  You can adjust num_indicies and indices_step_size to trade speed fo
        # accuracy. There is also a read_json_as_complex that will read in coordinates in JSON format directly.  You can modify
        # Daniel's Coding Train JavaScript coordinates to be JSON and that will run well.
        z = Epicycles.read_image_as_complex("img/mental.png", num_indicies=1700, indices_step_size=5)
        fourier_data = fourier.fft(z)
        # Sort so that largest epicycles are at the center, and the smaller ones are at the location of the drawing points
        fourier_data.sort(key=lambda x: x.amplitude, reverse=True)
        epicycles = Epicycles(fourier_data, plot_size=[427, 427])
        epicycles.run()
        time.sleep(5)
        #
        #make_gif(".", "branches.gif", "branches-*.png")
        #make_gif(".", "sudoku.gif", "sudoku*.jpg")
        #make_gif(".", "conway.gif", "conway-*.jpg")
        #
        hfp = open('header.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        #
        sfp = open('colete.gif', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        #
        return message

    @staticmethod
    def compose_email(sender_email, mailing_list, message_content, subject):
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
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = mailing_list
        # Create the plain-text and HTML version of your message
        body = MIMEMultipart("alternative")
        body.set_charset(cs)
        body.replace_header('Content-Transfer-Encoding', 'quoted-printable')
        #
        text = message_content
        html = "<br><img src='cid:header'><br>" + mistune.html(text) + "<br><img src='cid:signature'><br>"
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
        generate_art_samila()
        #
        #signature = Invader()
        #signature.run(17, 15, 427)
        #
        #sudoku = Sudoku()
        #sudoku.create()
        #sudoku.solve()
        #
        #gol = Conway()
        #gol.draw(427)
        #
        #generate_branches()
        #
        #generate_fourier_epicycles_drawing()
        #
        # Daniel's Coding Train JavaScript coordinates to be JSON and that will run well.
        z = Epicycles.read_image_as_complex("img/abuse.jpg", num_indicies=3400, indices_step_size=5)
        fourier_data = fft(z)
        # Sort so that largest epicycles are at the center, and the smaller ones are at the location of the drawing points
        fourier_data.sort(key=lambda x: x.amplitude, reverse=True)
        epicycles = Epicycles(fourier_data, plot_size=[1000, 1000])
        epicycles.run()
        time.sleep(3)
        #
        #make_gif(".", "branches.gif", "branches-*.png")
        #make_gif(".", "sudoku.gif", "sudoku*.jpg")
        #make_gif(".", "conway.gif", "conway-*.jpg")
        #
        hfp = open('header.png', 'rb')
        msg_image_header = MIMEImage(hfp.read())
        hfp.close()
        # Define the image's ID as referenced above
        msg_image_header.add_header('Content-ID', '<header>')
        message.attach(msg_image_header)
        #
        sfp = open('colete.gif', 'rb')
        msg_image_signature = MIMEImage(sfp.read())
        sfp.close()
        # Define the image's ID as referenced above
        msg_image_signature.add_header('Content-ID', '<signature>')
        message.attach(msg_image_signature)
        #
        return message
