import ascii_magic
import os
import sys


def generate_ascii(image_path):
    """Generate New Config

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
        img_path=image_path, columns=200, mode=ascii_magic.Modes.HTML
    )
    #
    ascii_magic.to_html_file("ascii.html", art, additional_styles="background: #222;")
    return art
