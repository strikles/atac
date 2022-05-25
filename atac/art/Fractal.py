from matplotlib import pyplot as plt
from matplotlib import colors

import numpy as np


class Fractal:
    """ """

    def mandelbrot(self, z, max_iter):
        """ """
        c = z
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z * z + c
        return max_iter

    def mandelbrot_set(self, x_min, x_max, y_min, y_max, width, height, max_iter):
        """ """
        r1 = np.linspace(x_min, x_max, width)
        r2 = np.linspace(y_min, y_max, height)
        n3 = np.empty((width, height))
        for i in range(width):
            for j in range(height):
                n3[i, j] = self.mandelbrot(r1[i] + 1j * r2[j], max_iter)
        return (r1, r2, n3)

    def mandelbrot_image(
        self, x_min, x_max, y_min, y_max, width=10, height=10, max_iter=80, cmap="hot"
    ):
        """ """
        dpi = 72
        img_width = dpi * width
        img_height = dpi * height
        x, y, z = self.mandelbrot_set(
            x_min, x_max, y_min, y_max, img_width, img_height, max_iter
        )
        #
        fig, ax = plt.subplots(figsize=(width, height), dpi=72)
        ticks = np.arange(0, img_width, 3 * dpi)
        x_ticks = x_min + (x_max - x_min) * ticks / img_width
        plt.xticks(ticks, x_ticks)
        y_ticks = y_min + (y_max - y_min) * ticks / img_width
        plt.yticks(ticks, y_ticks)
        #
        plt.axis("off")
        norm = colors.PowerNorm(0.3)
        ax.imshow(z.T, cmap=cmap, origin="lower")
        plt.show()
        self.save_image(fig)

    def save_image(self, fig):
        """ """
        filename = "mandelbrot.png"
        fig.savefig(filename)
        self.mandelbrot_image(-2.0, 0.5, -1.25, 1.25, cmap="viridis")
