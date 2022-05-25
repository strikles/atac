import random


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageSequence


class Invader:
    """ """

    def __init__(self):
        """ """
        self.origDimension = 1500
        self.r = lambda: random.randint(50, 255)
        self.rc = lambda: ("#%02X%02X%02X" % (self.r(), self.r(), self.r()))
        self.listSym = []

    #
    def create_square(self, border, draw, randColor, element, size):
        """ """
        if element == int(size / 2):
            draw.rectangle(border, randColor)
        elif len(self.listSym) == element + 1:
            draw.rectangle(border, self.listSym.pop())
        else:
            self.listSym.append(randColor)
            draw.rectangle(border, randColor)

    def create_invader(self, border, draw, size):
        """ """
        x0, y0, x1, y1 = border
        squareSize = (x1 - x0) / size
        randColors = [self.rc(), self.rc(), self.rc(), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        incrementer = 1
        element = 0
        #
        for y in range(0, size):
            incrementer *= -1
            element = 0
            for x in range(0, size):
                topLeftX = x * squareSize + x0
                topLeftY = y * squareSize + y0
                botRightX = topLeftX + squareSize
                botRightY = topLeftY + squareSize
                #
                self.create_square(
                    (topLeftX, topLeftY, botRightX, botRightY),
                    draw,
                    random.choice(randColors),
                    element,
                    size,
                )
                if element == int(size / 2) or element == 0:
                    incrementer *= -1
                element += incrementer

    def run(self, size, invaders, imgSize):
        """ """
        self.origDimension = imgSize
        origImage = Image.new("RGB", (self.origDimension, self.origDimension))
        draw = ImageDraw.Draw(origImage)
        #
        invaderSize = self.origDimension / invaders
        print(invaderSize)
        padding = invaderSize / size
        print(padding)
        # Will eventually create many
        finalBotRightX = 0
        finalBotRightY = 0
        for x in range(0, invaders):
            for y in range(0, invaders):
                topLeftX = x * invaderSize + padding
                topLeftY = y * invaderSize + padding
                botRightX = topLeftX + invaderSize - padding * 2
                botRightY = topLeftY + invaderSize - padding * 2
                #
                finalBotRightX = botRightX
                finalBotRightY = botRightY
                self.create_invader(
                    (topLeftX, topLeftY, botRightX, botRightY), draw, size
                )
        #    origImage.save("Examples/Example-"+str(size)+"x"+str(size)+"-"+str(invaders)+"-"+str(imgSize)+".jpg")
        origImage.crop((0, 0, botRightX - padding, botRightY - padding)).save(
            "signature.jpg"
        )
