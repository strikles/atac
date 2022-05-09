from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#
import os
import qrcode


num_calls = 0
def create_image(text, window_height, window_width):
    """ Generate Image from text

    Parameters
    ----------
    text : str
        The name of the animal
    window_height : int
        The image height
    window_width : int
    The image width
    """
    global num_calls
    img = Image.new('L', (window_height, window_width), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('fonts/LiberationMono-Bold.ttf', 31)
    draw.text((0, 0), text, font=font)
    img.save('sudoku{}.jpg'.format(num_calls))
    num_calls += 1


def make_gif(frame_folder, output_file_name, glob_pattern):
    """
    """
    frames = [Image.open(image) for image in glob.glob(f"{frame_folder}/{glob_pattern}")]
    frame_one = frames[0]
    frame_one.save(output_file_name, format="GIF", append_images=frames, save_all=True, duration=277, loop=0)
    print(">> make_gif" + os.path.join(
            os.path.dirname(__file__), output_file_name
    ))


def create_qr_code(url):
    """ Generate QR Code

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