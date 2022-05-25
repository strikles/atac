from .Art import Art

import random

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw


class Conway:
    """
    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
    conway's game of life
    """

    grid = []

    def gameOfLife(self):
        state = {}
        rows = len(self.grid)
        if rows == 0:
            return
        cols = len(self.grid[0])
        #
        for i in range(rows):
            for j in range(cols):
                an = 0
                cs = self.grid[i][j]
                if i - 1 >= 0 and j - 1 >= 0 and self.grid[i - 1][j - 1] == 1:
                    an += 1
                if i - 1 >= 0 and self.grid[i - 1][j] == 1:
                    an += 1
                if i - 1 >= 0 and j + 1 < cols and self.grid[i - 1][j + 1] == 1:
                    an += 1
                if i + 1 < rows and j - 1 >= 0 and self.grid[i + 1][j - 1] == 1:
                    an += 1
                if i + 1 < rows and self.grid[i + 1][j] == 1:
                    an += 1
                if i + 1 < rows and j + 1 < cols and self.grid[i + 1][j + 1] == 1:
                    an += 1
                if j - 1 >= 0 and self.grid[i][j - 1] == 1:
                    an += 1
                if j + 1 < cols and self.grid[i][j + 1] == 1:
                    an += 1
                #
                if an < 2 and cs == 1:
                    state[(i, j)] = 0
                elif an > 3 and cs == 1:
                    state[(i, j)] = 0
                elif an == 3 and cs == 0:
                    state[(i, j)] = 1
        #
        for k, v in state.items():
            self.grid[k[0]][k[1]] = v

    def randomState(self, rows, cols, alive):
        """ """
        state = {}
        tots = 0
        while tots < alive:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            if (r, c) in state:
                continue
            state[(r, c)] = 1
            tots += 1
        return state

    def initBoard(self, rows, cols, state):
        """ """
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        for k, v in state.items():
            self.grid[k[0]][k[1]] = v

    def draw(self, dimensions):
        """ """
        num_iters = 0
        self.initBoard(53, 95, self.randomState(53, 95, 1000))
        img = Image.new("L", (dimensions, dimensions), color="white")
        draw = ImageDraw.Draw(img)
        rows = len(self.grid)
        if rows == 0:
            return
        cols = len(self.grid[0])
        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j]:
                    draw.rectangle(
                        (5 + i * 10, 5 + j * 10, 13 + i * 10, 13 + j * 10), fill="black"
                    )
                    img.save("conway-{}.jpg".format(num_iters), "JPEG")
                    self.gameOfLife()
                    num_iters += 1
