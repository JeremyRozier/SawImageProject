import time
import numpy as np
import random

import matplotlib.animation as animation
from constants import *
import matplotlib.pyplot as plt
from decorators import store_time, dic_function_time


class GridAriane:
    """Class which defines and handles grids."""

    def __init__(self, length):
        """
        Grid's constructor :
            - map (numpy array) : contains the numpy array representing the grid.
            - pos (list) : [line, column] position/coordinates of the head of the SAW.
            - orientation (char) : direction where the head of the SAW is looking.
        """
        self.map = np.zeros((7, 7))
        self.pos = [3, 3]
        self.orientation = ""
        self.list_points_x = [3]
        self.list_points_y = [-3]
        self.map[3, 3] = 1
        self.delta0 = 0
        self.delta1 = 0
        self.rank = 1
        self.length = length
        self.biases = [0.25, 0.25, 0.25, 0.25]  # [N, S, E, W]

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.step = (self.length // 455) + 1

    @store_time
    def move(self):
        """Moves the SAW by 1 unit in the direction the head is looking."""
        line, column = DIC_ORIENTATION_COORDINATES[self.orientation][:2]
        self.pos[0] += line
        self.pos[1] += column
        self.list_points_y.append(-self.pos[0] - self.delta0)
        self.list_points_x.append(self.pos[1] + self.delta1)
        self.map[self.pos[0]][self.pos[1]] = self.rank

    @store_time
    def expand(self):
        """Expand the grid in the direction the head of the SAW is looking, also update coordinates when needed."""
        if self.orientation == 'E':
            self.map = np.concatenate((self.map, np.zeros((np.shape(self.map)[0], 1))), axis=1)

        elif self.orientation == 'W':
            self.map = np.concatenate((np.zeros((np.shape(self.map)[0], 1)), self.map), axis=1)
            self.pos[1] += 1
            self.delta1 -= 1

        elif self.orientation == 'S':
            self.map = np.concatenate((self.map, np.zeros((1, np.shape(self.map)[1]))), axis=0)

        elif self.orientation == 'N':
            self.map = np.concatenate((np.zeros((1, np.shape(self.map)[1])), self.map), axis=0)
            self.pos[0] += 1
            self.delta0 -= 1

    @store_time
    def probabilities(self, directions):
        same = True
        if len(directions) > 1:
            for elem in directions[1:]:
                if elem != directions[0]:
                    same = False
                    break
            if not same:
                if "N" in directions:
                    for i in range(int(self.biases[0] * 100)):
                        directions.append("N")
                if "S" in directions:
                    for i in range(int(self.biases[1] * 100)):
                        directions.append("S")
                if "E" in directions:
                    for i in range(int(self.biases[2] * 100)):
                        directions.append("E")
                if "W" in directions:
                    for i in range(int(self.biases[3] * 100)):
                        directions.append("W")
        return directions

    @store_time
    def get_possibilities(self):
        directions = []
        if self.map[self.pos[0] - 1][self.pos[1]] == 0:
            directions.append("N")
        if self.map[self.pos[0] + 1][self.pos[1]] == 0:
            directions.append("S")
        if self.map[self.pos[0]][self.pos[1] - 1] == 0:
            directions.append("W")
        if self.map[self.pos[0]][self.pos[1] + 1] == 0:
            directions.append("E")

        directions = self.probabilities(directions)
        return directions

    @store_time
    def backup(self):
        directions = ["N", "S", "E", "W"]
        for elem in directions:
            line, column = DIC_ORIENTATION_COORDINATES[elem][:2]
            if self.map[self.pos[0] + line][self.pos[1] + column] == self.rank - 1:
                self.pos = [self.pos[0] + line, self.pos[1] + column]
                self.rank -= 1
                self.list_points_x.pop(-1)
                self.list_points_y.pop(-1)
                break

    def run(self):
        moves = 1
        while moves <= self.length:
            print(moves, "({}%)".format(round(moves / self.length * 100)))
            possibilities = self.get_possibilities()
            if len(possibilities) == 0:
                self.backup()
                moves -= 1
            else:
                chosen = random.choice(possibilities)
                self.orientation = chosen
                self.rank += 1
                self.move()
                moves += 1
                if self.pos[0] == 2 or self.pos[0] == np.shape(self.map)[0] - 3:
                    self.expand()
                elif self.pos[1] == 2 or self.pos[1] == np.shape(self.map)[1] - 3:
                    self.expand()
        self.display_saw()

    def animate(self, i):
        """
        Animation of the saw with matplotlib.
        :param i : ith current frame of the animation (0 à FRAMES - 1).
        """

        self.ax.plot(self.list_points_x[(i - 1) * self.step - 1:i * self.step],
                     self.list_points_y[(i - 1) * self.step - 1:i * self.step],
                     c='black', linewidth=LINE_WIDTH)

    def display_saw(self):
        """
        Displays the whole way of the SAW made in the current grid.
        :return: None
        """
        anim = animation.FuncAnimation(self.fig, self.animate, frames=910, interval=33)
        anim.save("saw_animation.gif", writer="ffmpeg")



grid = GridAriane(10000)
t1 = time.time()
grid.run()
print(f"the whole program took {time.time() - t1} seconds.")
for function, list_seconds in dic_function_time.items():
    print(f"Time took by {function} : {sum(list_seconds)} seconds.")


