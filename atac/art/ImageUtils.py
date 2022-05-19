import glob
import json
import os
import qrcode
#
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


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


def add_margin(pil_img, top, right, bottom, left, color):
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result


def make_gif(frame_folder, output_file_name, glob_pattern):
    """
    """
    gif_filename = os.path.join(frame_folder, output_file_name)
    try:
        image_paths = [os.path.join(frame_folder, f) for f in sorted(os.listdir(frame_folder)) if os.path.isfile(os.path.join(frame_folder, f))]
        print(json.dumps(image_paths, indent=4))
        raw_frames = [Image.open(path).convert('RGB') for path in image_paths]
        frames = list(map(lambda i: add_margin(i, 0, max(0, int(0.5*(500-i.size[0]))), 0, int(max(0, 0.5*(500-i.size[0]))), (255,255,255)), raw_frames))
        #
        if not len(frames):
            print("cannot create gif for: " + gif_filename)
            exit(1)
        frame_one = frames[0]
        frame_one.save(gif_filename, format="GIF", append_images=frames, save_all=True, duration=1000, loop=0)
        #
        if os.path.isfile(gif_filename):
            print(">> made gif: " + output_file_name)
        else:
            print(">> gif creation failed: " + output_file_name)    
    except IOError:
        print("cannot create gif for:" + gif_filename)


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