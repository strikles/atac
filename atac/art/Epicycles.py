"""
Python implementation of Drawing With Fourier Epicycles, based on Coding Train Tutorial by Daniel Shiffman:
https://thecodingtrain.com/CodingChallenges/130.3-fourier-transform-drawing.html

Uses drawing coordinate extraction algorithm from Randy Olson:
http://www.randalolson.com/2018/04/11/traveling-salesman-portrait-in-python/

MIT License
"""
from ..util.Util import *
import json
import numpy as np
import math
import cmath
import os
import time
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import animation
from PIL import Image, ImageOps, ImageFilter
from tsp_solver.greedy_numpy import solve_tsp
from scipy.spatial.distance import pdist, squareform

# plt.style.use('dark_background')


class Epicycles:
    """Fourier Epicycle drawing class, modeled after:

    https://thecodingtrain.com/CodingChallenges/130.3-fourier-transform-drawing.html
    """

    def __init__(self, fourier_data, plot_size):
        """Constructor

        :param fourier_data Array of FourierDatum
        :param plot_size The [x, y] plot size to use
        """
        n = len(fourier_data)
        self.phase = 0
        self.fourier_data = fourier_data
        # holds coordinates of drawing at the end of the last epicycle
        self.x_drawing_positions = []
        self.y_drawing_positions = []
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=(0, plot_size[0]), ylim=(0, plot_size[1]))
        # line plot for x/y drawing_data
        (self.drawing_line,) = self.ax.plot([], [], lw=1.5)
        self.epicycles = np.zeros(n, dtype=[("position", float, 2), ("size", float, 1)])
        # for lines from epicycle center to next epicycle
        self.epicycle_lines = [
            Line2D([], [], color="orange", lw=0.7, alpha=0.7) for count in range(n)
        ]
        # scatter plot for epicycles
        self.epicycle_scatter = self.ax.scatter(
            self.epicycles["position"][:, 0],
            self.epicycles["position"][:, 1],
            s=self.epicycles["size"],
            lw=0.7,
            edgecolors="red",
            facecolors="black",
            alpha=0.7,
        )
        # dont show axes and invert for imagery upper-left origin
        self.ax.axis("off")
        self.ax.invert_yaxis()
        # create plots for lines within epicycle
        for epicycle_line in self.epicycle_lines:
            self.ax.add_line(epicycle_line)

    @staticmethod
    def read_json_as_complex(json_file_path):
        """Reads JSON array of x/y points as complex numbers

        :param json_file_path Absolute path to JSON file
        :returns Image outline indices as complex numbers
        """

        with open(json_file_path) as json_file:
            data = json.load(json_file)
        #
        z = []
        for i in range(0, len(data)):
            z.append(complex(data[i]["x"], data[i]["y"]))
        #
        return z

    @staticmethod
    def read_image_as_complex(image_file_path, num_indicies=1700, indices_step_size=5):
        """Read image outline into complex numbers.

        Uses random num_indicies locations to create outline of image
        :param num_indicies The number of random indicies to select from the image outline
        :param indicies_step_size The step size to use for excluding indicies.  Select higher value to reduce data size,
        DFT size, and computation time of epicycles, at the cost of drawing accuracy.
        :returns Image outline indices as complex numbers
        """

        # Image drawing point extraction algorithm from Randy Olson:
        # http://www.randalolson.com/2018/04/11/traveling-salesman-portrait-in-python/

        # Convert image to black and white
        image = Image.open(image_file_path, "r")
        bw_image = image.convert("1", dither=Image.NONE)
        # bw_image = ImageOps.grayscale(image)
        # plt.imshow(bw_image)
        # Identify black pixels and select random subset of them
        bw_image_array = np.array(bw_image, dtype=np.int)
        black_indices = np.argwhere(bw_image_array == 0)
        #
        chosen_black_indices = black_indices[
            np.random.choice(
                black_indices.shape[0],
                replace=False,
                size=num_indicies
                if num_indicies <= black_indices.shape[0]
                else black_indices.shape[0],
            )
        ]
        # Find path between black pixels by solving the Traveling Salesman Problem
        distances = pdist(chosen_black_indices)
        distance_matrix = squareform(distances)
        #
        print("Solving traveling salesman problem for drawing path...")
        optimized_path = solve_tsp(distance_matrix)
        print("Done solving traveling salesman.")
        optimized_path_points = [chosen_black_indices[x] for x in optimized_path]
        # Plot the traveling salesman path of the points to draw
        """
        plt.figure()
        plt.scatter([x[1] for x in chosen_black_indices], [x[0] for x in chosen_black_indices], color='red', s=1)
        plt.gca().invert_yaxis()
        plt.xticks([])
        plt.yticks([])
        """
        # Save the black pixel path (x, y) coordinates as complex numbers
        z = []
        for i in range(0, len(optimized_path_points), indices_step_size):
            z.append(complex(optimized_path_points[i][1], optimized_path_points[i][0]))
        #
        return z

    def _draw(self, frame):
        """Draw the epicycles, drawing points, and epicycle lines

        :param frame The animation frame number
        """

        # put the first epicycle at (100, 100)
        x = 1
        y = 1
        # Calculate epicycle positions and sizes based on DFT data and the current self.phase
        i = 0
        #
        for fourier_datum in self.fourier_data:
            prev_x = x
            prev_y = y
            radius = fourier_datum.amplitude
            x += radius * np.cos(fourier_datum.freq * self.phase + fourier_datum.phase)
            y += radius * np.sin(fourier_datum.freq * self.phase + fourier_datum.phase)
            self.epicycles["position"][i] = [prev_x, prev_y]
            self.epicycles["size"][i] = radius * 2
            self.epicycle_lines[i].set_data([prev_x, x], [prev_y, y])
            i += 1
        # Setting the data will draw the epicycles
        self.epicycle_scatter.set_sizes(self.epicycles["size"])
        self.epicycle_scatter.set_offsets(self.epicycles["position"])
        # Draw the output image outline at the last epicycle position
        self.x_drawing_positions.append(x)
        self.y_drawing_positions.append(y)
        self.drawing_line.set_data(self.x_drawing_positions, self.y_drawing_positions)
        #
        phase_delta = 2 * np.pi / len(self.fourier_data)
        self.phase += phase_delta
        #
        if self.phase > 2 * np.pi:
            # freeze at completion for 3 seconds and then restart the drawing
            time.sleep(3)
            self.phase = 0
            self.x_drawing_positions = []
            self.y_drawing_positions = []
        #
        return (
            self.drawing_line,
            self.epicycle_lines,
            self.epicycle_scatter,
        )

    def run(self):
        """Runs the Epicycle animation"""
        if not os.path.isfile("colete.gif"):
            a = animation.FuncAnimation(
                self.fig, self._draw, frames=len(self.fourier_data), interval=20
            )
            a.save("colete.gif", writer="imagemagick")
