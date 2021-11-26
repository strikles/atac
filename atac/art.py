#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generative Art Stuff.

@author: strikles
"""

import ascii_magic
import math
import markovify
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import os

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import qrcode
import random
from samila import GenerativeImage
from scipy.io import wavfile
import spacy
from spacy.matcher import Matcher
import syllapy
import sys
import utils


def generate_haiku():
    """
    """
    nlp = spacy.load("en_core_web_sm")
    matcher2 = Matcher(nlp.vocab)
    matcher3 = Matcher(nlp.vocab)
    matcher4 = Matcher(nlp.vocab)
    #
    pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
               {'POS':  {"IN": ["NOUN", "VERB"]} }]
    matcher2.add("TwoWords", [pattern])
    pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
               {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
               {'POS':  {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }]
    matcher3.add("ThreeWords", [pattern])
    pattern = [{'POS':  {"IN": ["NOUN", "ADP", "ADJ", "ADV"]} },
               {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
               {'IS_ASCII': True, 'IS_PUNCT': False, 'IS_SPACE': False},
               {'POS':  {"IN": ["NOUN", "VERB", "ADJ", "ADV"]} }]
    matcher4.add("FourWords", [pattern])
    #
    doc = nlp(open("data/orwell_1984.txt").read())
    #
    matches2 = matcher2(doc)
    matches3 = matcher3(doc)
    matches4 = matcher4(doc)
    #
    g_5 = []
    g_7 = []
    #
    for match_id, start, end in matches2 + matches3 + matches4:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        #
        syl_count = 0
        for token in span:
            syl_count += syllapy.count(token.text)
        if syl_count == 5:
            if span.text not in g_5:
                g_5.append(span.text)
        if syl_count == 7:
            if span.text not in g_7:
                g_7.append(span.text)
    #
    print("Enter for a new haiku. ^C to quit\n")
    while (True):
        print("%s\n%s\n%s" %(random.choice(g_5),random.choice(g_7),random.choice(g_5)))
        input("\n")

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


def generate_art_samila():
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


def twinkle_sine():
    """
    """
    right_hand_notes = ['C4', 'C4', 'G4', 'G4',
                       'A4', 'A4', 'G4',
                       'F4', 'F4', 'E4', 'E4',
                       'D4', 'D4', 'C4',
                       'G4', 'G4', 'F4', 'F4',
                       'E4', 'E4', 'D4',
                       'G4', 'G4', 'F4', 'F4',
                       'E4', 'E4', 'D4',
                       'C4', 'C4', 'G4', 'G4',
                       'A4', 'A4', 'G4',
                       'F4', 'F4', 'E4', 'E4',
                       'D4', 'D4', 'C4',]
    right_hand_duration = [0.5, 0.5, 0.5, 0.5,
                           0.5, 0.5, 1]*6
    #
    left_hand_notes = ['C3',
                      'A3',
                      'F3',
                      'D3', 'C3',
                      'G3', 'F3',
                      'E3', 'D3',
                      'G3', 'F3',
                      'E3', 'D3',
                      'C3', 'E3', 'G3', 'C4',
                      'A3', 'A3', 'G3',
                      'F3', 'B2', 'E3', 'C3',
                      'D3', 'D3', 'C3']
    #
    left_hand_duration = [2,
                          2,
                          2,
                          1, 1,
                          1, 1,
                          1, 1,
                          1, 1,
                          1, 1,
                          0.5, 0.5, 0.5, 0.5,
                          0.5, 0.5, 1,
                          0.5, 0.5, 0.5, 0.5,
                          0.5, 0.5, 1]
    #
    factor = [0.68, 0.26, 0.03, 0.  , 0.03]
    length = [0.01, 0.6, 0.29, 0.1]
    decay = [0.05,0.02,0.005,0.1]
    sustain_level = 0.1
    #
    right_hand = utils.get_song_data(right_hand_notes, right_hand_duration, 2,
                                     factor, length, decay, sustain_level)
    factor = [0.73, 0.16, 0.06, 0.01, 0.02, 0.01  , 0.01]
    length = [0.01, 0.29, 0.6, 0.1]
    decay = [0.05,0.02,0.005,0.1]
    left_hand = utils.get_song_data(left_hand_notes, left_hand_duration, 2,
                                     factor, length, decay, sustain_level)
    data = left_hand+right_hand
    data = data * (4096/np.max(data))
    #
    wavfile.write('data/twinkle_star.wav', 44100, data.astype(np.int16))


class Fractal:
    """
    """

    def mandelbrot(self, z, max_iter):
        """
        """
        c = z
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter

    def mandelbrot_set(self, x_min, x_max, y_min, y_max, width, height, max_iter):
        """
        """
        r1 = np.linspace(x_min, x_max, width)
        r2 = np.linspace(y_min, y_max, height)
        n3 = np.empty((width, height))
        for i in range(width):
            for j in range(height):
                n3[i,j] = self.mandelbrot(r1[i] + 1j*r2[j], max_iter)
        return (r1, r2, n3)

    def mandelbrot_image(self, x_min, x_max, y_min, y_max, width=10, height=10, max_iter=80, cmap='hot'):
        """
        """
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

    def save_image(self, fig):
        """
        """
        filename = "mandelbrot.png"
        fig.savefig(filename)
        self.mandelbrot_image(-2.0, 0.5, -1.25, 1.25, cmap='viridis')


class Invader:
    """
    """
    def __init__(self):
        """
        """
        self.origDimension = 1500
        self.r = lambda: random.randint(50,255)
        self.rc = lambda: ('#%02X%02X%02X' % (self.r(),self.r(),self.r()))
        self.listSym = []
    #
    def create_square(self, border, draw, randColor, element, size):
        """
        """
        if (element == int(size/2)):
            draw.rectangle(border, randColor)
        elif (len(self.listSym) == element+1):
            draw.rectangle(border,self.listSym.pop())
        else:
            self.listSym.append(randColor)
            draw.rectangle(border, randColor)

    def create_invader(self, border, draw, size):
        """
        """
        x0, y0, x1, y1 = border
        squareSize = (x1-x0)/size
        randColors = [self.rc(), self.rc(), self.rc(), (0,0,0), (0,0,0), (0,0,0)]
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

    def run(self, size, invaders, imgSize):
        """
        """
        self.origDimension = imgSize
        origImage = Image.new('RGB', (self.origDimension, self.origDimension))
        draw = ImageDraw.Draw(origImage)
        #
        invaderSize = self.origDimension/invaders
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
                #
                finalBotRightX = botRightX
                finalBotRightY = botRightY
                self.create_invader((topLeftX, topLeftY, botRightX, botRightY), draw, size)
        #    origImage.save("Examples/Example-"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")
        origImage.crop((0, 0, botRightX-padding, botRightY-padding)).save("Examples/paddingTest.jpg")
