import math
import random
from samila import GenerativeImage


def generate_art_samila():
    """ """

    def f1(x, y):
        result = random.uniform(-1, 1) * x**2 - math.sin(y**2) + abs(y - x)
        return result

    def f2(x, y):
        result = random.uniform(-1, 1) * y**3 - math.cos(x**2) + 2 * x
        return result

    #
    g = GenerativeImage(f1, f2)
    g.generate()
    g.plot()
    status = g.save_image(file_adr="header.png")
    #
    return status
