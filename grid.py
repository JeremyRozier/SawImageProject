import numpy as np
import random
from statistics import Statistics
from constants import *
import matplotlib.pyplot as plt


class Grid:
    """Class which defines and handles grids."""

    def __init__(self, size: int, expandable: bool):
        """
        Grid's constructor :
            - map (numpy array) : contains the numpy array representing the grid.
            - pos (list) : [line, column] position/coordinates of the head of the SAW.
            - dim_shape (tuple[int]) : contains the length of each map's dimension (1D, 2D, 3D...).
            - orientation (char) : direction where the head of the SAW is looking.
            - dic_statistics (dict) : dic which contains statistics of the SAW
             (can be saved out of the class).

        :param size: square size of the grid.
        :param expandable: indicates whether the grid is expandable or not

        """
        self.size = size  # grid size (square)
        self.expandable = expandable
        self.map = np.zeros((self.size, self.size))
        self.pos = [self.size // 2, self.size // 2]
        self.list_points = [(self.size // 2, self.size // 2)]
        self.dim_shape = tuple(reversed(np.shape(self.map)))
        self.orientation = "E"
        self.dic_statistics = DIC_DATA

    def clear(self):
        """Resets the grid to be all 0 (grid size remain the same)."""
        self.map *= 0
        self.pos = [self.size // 2, self.size // 2]
        self.list_points = [(self.pos[0], self.pos[1])]

    def move(self):
        """Moves the SAW by 1 unit in the direction the head is looking."""
        line, column = DIC_ORIENTATION_COORDINATES[self.orientation][:2]
        self.pos[0] += line
        self.pos[1] += column
        self.list_points.append((self.pos[0], self.pos[1]))
        self.map[self.pos[0]][self.pos[1]] = 1

    def expand(self):
        """Expands the grid by one unit in the direction the head of the SAW is looking."""
        axis = DIC_ORIENTATION_COORDINATES[self.orientation][2]
        if axis == 0:
            self.map = np.concatenate((np.zeros((1, self.dim_shape[axis])), self.map), axis=axis)
        elif axis == 1:
            self.map = np.concatenate((np.zeros((self.dim_shape[axis]), 1), self.map), axis=axis)

    def get_possibilities(self):
        """
        Gets available orientations around the head of the SAW.
        :return: list[chars] (ex : ['N', 'S'])
        """
        list_possibilities = []
        list_limit_cases = []

        if self.pos[0] == 0:
            list_limit_cases.append("N")
        if self.pos[0] == np.shape(self.map)[0] - 1:
            list_limit_cases.append("S")
        if self.pos[1] == 0:
            list_limit_cases.append("W")
        if self.pos[1] == np.shape(self.map)[1] - 1:
            list_limit_cases.append("E")

        for orientation, coords in DIC_ORIENTATION_COORDINATES.items():
            line, column = coords[:2]

            if orientation in list_limit_cases:
                continue

            if self.map[self.pos[0] + line][self.pos[1] + column] == 1:
                continue

            list_possibilities.append(orientation)

        return list_possibilities

    def display_saw(self, moves: int):
        """
        Displays the whole way of the SAW made in the current grid.

        :param moves: number of moves made by the saw (could be interesting for line width)
        :return:
        """
        list_coords_x = [x for x, y in self.list_points]
        list_coords_y = [y for x, y in self.list_points]

        """x_min, x_max = min(list_coords_x), max(list_coords_x)
        y_min, y_max = min(list_coords_y), max(list_coords_y)"""

        plt.plot(list_coords_x, list_coords_y, linewidth=LINE_WIDTH)
        plt.show()

    def test(self, tries=NB_TRIES, maximum_moves=MAXIMUM_MOVES):
        """
        Runs tests with the self avoiding walks.

        :param tries: number of tries.
        :param maximum_moves: maximum amount of moves.

        :return: None
        """

        attempt = 0
        max_moves = 0
        min_moves = maximum_moves
        moves_per_try = []
        density = []
        got_blocked = []

        while attempt < tries:
            self.clear()
            moves = 0
            blocked = False

            while (not blocked) and (moves < maximum_moves):
                list_possibilities = self.get_possibilities()
                self.orientation = random.choice(list_possibilities) if len(list_possibilities) > 0 else None
                if self.orientation is None:
                    blocked = True
                    self.display_saw(moves)
                    break
                self.move()
                moves += 1
                if self.expandable:
                    if self.pos[0] == 0 or self.pos[0] == np.shape(self.map)[0] - 1:
                        self.expand()
                    elif self.pos[1] == 0 or self.pos[1] == np.shape(self.map)[1] - 1:
                        self.expand()

            if blocked:
                got_blocked.append(1)
            else:
                got_blocked.append(0)

            moves_per_try.append(moves)
            density.append(np.sum(self.map) / np.size(self.map))

            if max_moves < moves:
                max_moves = moves

            if min_moves > moves:
                min_moves = moves

            attempt += 1

        moves_per_try = np.array(moves_per_try)
        density = np.array(density)
        average_moves = np.sum(moves_per_try) / np.size(moves_per_try)
        average_density = np.sum(density) / np.size(density)

        self.dic_statistics = {"average_moves": average_moves,
                               "average_density": average_density,
                               "min_moves": min_moves,
                               "max_moves": max_moves
                               }

        save_response = input("Do you want to save statistics ? : ").lower()
        if save_response[0] == "o":
            Statistics.save(size=self.size, dic_to_save=self.dic_statistics, data_filename=DATA_FILENAME)

        return


if __name__ == "__main__":
    """for size in range(2, 256):
        plan = Grid(size, False)
        plan.test(NB_TRIES, MAXIMUM_MOVES)
        print(f"{255 - size} left")"""
    plan = Grid(1000, False)
    plan.test()

