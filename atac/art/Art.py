import glob
import io
import json
import os
import qrcode

import random

# from lib.util.io import loadJSON, pathExists
#
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageSequence

from ..config.Config import Config
from ..util.Util import *


class Art(Config):
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

    def __init__(self, encrypted_config=True, config_file_path="auth.json", key_file_path=None):
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

    def make_gif_from_dir(self, frame_folder, output_file_name, glob_pattern):
        """ """
        gif_filename = os.path.join(frame_folder, output_file_name)
        try:
            glob_arg = "{}/{}".format(os.path.abspath(frame_folder), glob_pattern)
            print("glob pattern: " + glob_arg)
            image_paths = [os.path.join(frame_folder, f) for f in sorted(glob.glob(glob_arg))]
            print(json.dumps(image_paths, indent=4))
            raw_frames = [Image.open(path).convert("RGB") for path in image_paths]
            frames = list(
                map(
                    lambda i: self.add_margin(
                        i,
                        0,
                        max(0, int(0.5 * (500 - i.size[0]))),
                        0,
                        int(max(0, 0.5 * (500 - i.size[0]))),
                        (255, 255, 255),
                    ),
                    raw_frames,
                )
            )
            #
            if not len(frames):
                print("no frames to create gif: " + gif_filename)
                return
            #
            frame_one = frames[0]
            frame_one.save(
                gif_filename,
                format="GIF",
                append_images=frames,
                save_all=True,
                duration=1000,
                loop=0,
            )
            #
            if os.path.isfile(gif_filename):
                print(">> made gif: " + output_file_name)
            else:
                print(">> gif creation failed: " + output_file_name)
        except IOError:
            print("cannot create gif for:" + gif_filename)
            exit(1)

    def generate_gifs_from_all_dirs(self, images_directory, glob_pattern):
        print(images_directory)
        subfolders = [f.path for f in os.scandir(os.path.abspath(images_directory)) if f.is_dir()]
        print(json.dumps(subfolders, indent=4))
        for subfolder_path in subfolders:
            print("{} - {}: ".format(subfolder_path, os.path.basename(subfolder_path)))
            gif_filename = "{}.{}".format(os.path.basename(subfolder_path), "gif")
            self.make_gif_from_dir(subfolder_path, gif_filename, glob_pattern)

    def add_centered_text_to_gif(self, gif_file_path, msg, font_size):
        #
        im = Image.open(gif_file_path)
        # A list of the frames to be outputted
        frames = []
        # Loop over each frame in the animated image
        for frame in ImageSequence.Iterator(im):
            # resize
            baseheight = 300
            hpercent = baseheight / float(frame.size[1])
            wsize = int((float(frame.size[0]) * float(hpercent)))
            frame = frame.resize((wsize, baseheight), Image.ANTIALIAS)
            # convert
            if frame.mode != "RGB":
                frame.convert("RGB")
            #
            frames.append(frame)
        #
        frames[0].save(gif_file_path, save_all=True, append_images=frames[1:])
        #
        im = Image.open(gif_file_path)
        # A list of the frames to be outputted
        frames = []
        # Loop over each frame in the animated image
        for frame in ImageSequence.Iterator(im):
            # draw
            W, H = (frame.size[0], frame.size[1])
            # Draw the text on the frame
            draw = ImageDraw.Draw(frame)
            font = ImageFont.truetype("fonts/LiberationMono-Bold.ttf", font_size)
            w, h = draw.textsize(msg, font)
            draw.text(((W - w) / 2, (H - h) / 2), msg, fill=211, font=font)
            del draw
            # However, 'frame' is still the animated image with many frames
            # It has simply been seeked to a later frame
            # For our list of frames, we only want the current frame
            # Saving the image without 'save_all' will turn it into a single frame image, and we can then re-open it
            # To be efficient, we will save it to a stream, rather than to file
            b = io.BytesIO()
            frame.save(b, format="GIF")
            frame = Image.open(b)
            # Then append the single frame image to a list of frames
            frames.append(frame)
        # Save the frames as a new image
        frames[0].save(gif_file_path, save_all=True, append_images=frames[1:])

    @staticmethod
    def create_image_from_text(
        text,
        window_height,
        window_width,
        background_color,
        foreground_color,
        output_file_path,
    ):
        """Generate Image from text

        Parameters
        ----------
        text : str
            The name of the animal
        window_height : int
            The image height
        window_width : int
        The image width
        """
        img = Image.new("L", (window_height, window_width), color=background_color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/LiberationMono-Bold.ttf", 31)
        draw.text((0, 0), text, fill=foreground_color, font=font)
        img.save(output_file_path)

    def add_margin(self, pil_img, top, right, bottom, left, color):
        width, height = pil_img.size
        new_width = width + right + left
        new_height = height + top + bottom
        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top))
        return result

    def create_qr_code(url):
        """Generate QR Code

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
