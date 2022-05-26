import random
import time

from .Art import Art


class Sudoku:
    """ """

    def __repr__(self):
        return "Sudoku()"

    def __str__(self):
        """ """
        res = ""
        for i, line in enumerate(self.board):
            if i % self.dim == 0:
                res += "\n"
            res += "|{}|{}|{}| |{}|{}|{}| |{}|{}|{}|\n".format(
                *(cell or " " for cell in line)
            )
        return res

    def __init__(self, dim=3):
        """ """
        self.dim = dim
        self.board = None
        self.numbers = range(1, dim**2 + 1)
        self.num_solve_calls = 0

    def createF(self):
        """Return a random filled dim**2 x dim**2 Sudoku board"""
        n = self.dim**2
        self.board = [[None for _ in range(n)] for _ in range(n)]

        def search(c=0):
            """ """
            i, j = divmod(c, n)
            i0, j0 = i - i % 3, j - j % 3  # Origin of mxm block
            numbers = list(range(1, n + 1))
            random.shuffle(numbers)
            for x in numbers:
                if (
                    x not in self.board[i]  # row
                    and all(row[j] != x for row in self.board)  # column
                    and all(
                        x not in row[j0 : j0 + self.dim]  # block
                        for row in self.board[i0:i]
                    )
                ):
                    self.board[i][j] = x
                    if c + 1 >= n**2 or search(c + 1):
                        return self.board
            else:
                # No number is valid in this cell: backtrack and try again.
                self.board[i][j] = None
                return None

        #
        return search()

    def create(self, difficulty="easy"):
        """ """
        self.createF()
        if difficulty == "easy":
            for i in range(30):
                iX = random.randrange(0, self.dim**2)
                iY = random.randrange(0, self.dim**2)
                self.board[iX][iY] = "."
        elif difficulty == "medium":
            for i in range(50):
                iX = random.randrange(0, self.dim**2)
                iY = random.randrange(0, self.dim**2)
                self.board[iX][iY] = "."
        elif difficulty == "hard":
            for i in range(80):
                iX = random.randrange(0, self.dim**2)
                iY = random.randrange(0, self.dim**2)
                self.board[iX][iY] = "."

    def createStatic(self):
        """ """
        self.dim = 3
        self.board = [
            [None for _ in range(self.dim**2)] for _ in range(self.dim**2)
        ]
        #
        self.board[0] = [".", 3, ".", ".", ".", ".", ".", ".", "."]
        self.board[1] = [".", ".", ".", 1, 9, 5, ".", ".", "."]
        self.board[2] = [".", ".", 8, ".", ".", ".", ".", 6, "."]
        #
        self.board[3] = [8, ".", ".", ".", 6, ".", ".", ".", "."]
        self.board[4] = [4, ".", ".", 8, ".", ".", ".", ".", 1]
        self.board[5] = [".", ".", ".", ".", 2, ".", ".", ".", "."]
        #
        self.board[6] = [".", 6, ".", ".", ".", ".", 2, 8, "."]
        self.board[7] = [".", ".", ".", 4, 1, 9, ".", ".", 5]
        self.board[8] = [".", ".", ".", ".", ".", ".", ".", 7, "."]

    def findNextCell(self, x, y):
        """ """
        for i in range(x, self.dim**2):
            for j in range(y, self.dim**2):
                if self.board[i][j] == ".":
                    return i, j
        for i in range(0, self.dim**2):
            for j in range(0, self.dim**2):
                if self.board[i][j] == ".":
                    return i, j
        return -1, -1

    def isValid(self, x, y, value):
        """ """
        rowValid = all([value != self.board[x][i] for i in range(self.dim**2)])
        if rowValid:
            columnValid = all([value != self.board[i][y] for i in range(self.dim**2)])
            if columnValid:
                subGridTopX, subGridTopY = int(3 * (x // 3)), int(3 * (y // 3))
                for i in range(subGridTopX, subGridTopX + 3):
                    for j in range(subGridTopY, subGridTopY + 3):
                        if self.board[i][j] == value:
                            return False
                return True
        return False

    def solve(self, x=0, y=0, show_each_step=True):
        """ """
        x, y = self.findNextCell(x, y)
        if show_each_step:
            print(self)
            self.num_calls += 1
            Art.create_image_from_text(self.__str__(), 427, 427, "sudoku_{}".format(self.num_solve_calls))
            time.sleep(0.3)
        if x == -1:
            return True
        for value in self.numbers:
            if self.isValid(x, y, value):
                self.board[x][y] = value
                if self.solve(x, y, show_each_step):
                    return True
                self.board[x][y] = "."
                return False
