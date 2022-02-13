import numpy as np
import random

from typing import List

from statistics import Statistics
from constants import *
import matplotlib.pyplot as plt


class Grid:
    """Class which defines and handles grids."""

    def __init__(self, size: int):
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
        self.size = size
        self.map = np.zeros((self.size, self.size))
        self.pos = [self.size - 4, self.size - 4]
        self.list_points = [(self.size // 2, self.size // 2)]
        self.dim_shape = tuple(reversed(np.shape(self.map)))
        self.orientation = "E"
        self.dic_statistics = DIC_DATA
        self.map[self.pos[0], self.pos[0]] = 1

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

    def expand(self):  # expend the grid by one unit in the direction the head of the SAW is looking
        if self.orientation == 'E':
            self.map = np.concatenate((self.map, np.zeros((np.shape(self.map)[0], 1))), axis=1)
        elif self.orientation == 'W':
            self.map = np.concatenate((np.zeros((np.shape(self.map)[0], 1)), self.map), axis=1)
            self.pos[1] += 1
        elif self.orientation == 'S':
            self.map = np.concatenate((self.map, np.zeros((1, np.shape(self.map)[1]))), axis=0)
        elif self.orientation == 'N':
            self.map = np.concatenate((np.zeros((1, np.shape(self.map)[1])), self.map), axis=0)
            self.pos[0] += 1

    def get_possibilities(self, coord: List[int]):
        """
        Gets available orientations around the given coordinates.
        :return: list[chars] (ex : ['N', 'S'])
        """
        list_possibilities = []
        list_limit_cases = []

        if coord[0] == 0:
            list_limit_cases.append("N")
        if coord[0] == np.shape(self.map)[0] - 1:
            list_limit_cases.append("S")
        if coord[1] == 0:
            list_limit_cases.append("W")
        if coord[1] == np.shape(self.map)[1] - 1:
            list_limit_cases.append("E")

        for orientation, coords in DIC_ORIENTATION_COORDINATES.items():
            line, column = coords[:2]

            if orientation in list_limit_cases:
                continue

            if self.map[coord[0] + line][coord[1] + column] == 1:
                continue

            list_possibilities.append(orientation)

        return list_possibilities

    def see_infinity(self, coord: List[int]):
        """
        Tells in which direction a given coordinate have a straight path to infinity.
        :param coord: list[ints] (ex : [-2, 6])
        :return: list[chars] (ex : ['N', 'S'])
        """
        directions = []

        if np.sum(self.map[coord[0]][coord[1] + 1:]) == 0:
            directions.append('E')
        if np.sum(self.map[coord[0]][:coord[1]]) == 0:
            directions.append('W')
        if np.sum(self.map.T[coord[1]][coord[0] + 1:]) == 0:
            directions.append('S')
        if np.sum(self.map.T[coord[1]][:coord[0]]) == 0:
            directions.append('N')

        return directions

    def fill_distances(self, area, current):
        """used in pathfinding"""
        if current == -5:
            return area
        for i in range(5):
            for j in range(5):
                if area[i][j] == current:
                    if i > 0:
                        if area[i - 1][j] == 0:
                            area[i - 1][j] = current - 1
                    if i < 4:
                        if area[i + 1][j] == 0:
                            area[i + 1][j] = current - 1
                    if j > 0:
                        if area[i][j - 1] == 0:
                            area[i][j - 1] = current - 1
                    if j < 4:
                        if area[i][j + 1] == 0:
                            area[i][j + 1] = current - 1
        area = self.fill_distances(area, current - 1)
        return area

    def pathfinding(self, start_coord, end_coord):
        """
        Checks in a 5 by 5 area centered on the starting coordinates for a path to the ending coordinates
        :param start_coord: list[ints] (ex : [-2, 6])
        :param end_coord: list[ints] (ex : [-1, 5])
        :return: list[list[ints]] or None (ex : [[-2, 6], [-2, 5], [-1, 5]])
        """
        if start_coord[0] == end_coord[0] and start_coord[1] == end_coord[1]:
            return []
        area = np.array([self.map[start_coord[0] + i][start_coord[1] - 2:start_coord[1] + 3] for i in range(-2, 3, 1)])
        end_coord = np.array(end_coord) - np.array(start_coord) + np.array([2, 2])
        delta = np.array(start_coord) - np.array([2, 2])
        start_coord = np.array([2, 2])
        area[end_coord[0]][end_coord[1]] = -1
        area = self.fill_distances(area, -1)
        if area[start_coord[0]][start_coord[1]] == 0:
            return None
        path = [start_coord]
        distance = area[start_coord[0]][start_coord[1]]
        while distance != -2:
            if path[-1][0] > 0:
                if area[path[-1][0] - 1][path[-1][1]] == distance + 1:
                    path.append([path[-1][0] - 1, path[-1][1]])
                    distance += 1
                    continue
            if path[-1][0] < 4:
                if area[path[-1][0] + 1][path[-1][1]] == distance + 1:
                    path.append([path[-1][0] + 1, path[-1][1]])
                    distance += 1
                    continue
            if path[-1][1] > 0:
                if area[path[-1][0]][path[-1][1] - 1] == distance + 1:
                    path.append([path[-1][0], path[-1][1] - 1])
                    distance += 1
                    continue
            if path[-1][1] < 4:
                if area[path[-1][0]][path[-1][1] + 1] == distance + 1:
                    path.append([path[-1][0], path[-1][1] + 1])
                    distance += 1
                    continue
        path.pop(0)
        for i in range(len(path)):
            path[i] += delta
        return path

    def display_saw(self, moves: int):
        """
        Displays the whole way of the SAW made in the current grid.
        :param moves: number of moves made by the saw (could be interesting for line width)
        :return: None
        """
        list_coords_x = [x for x, y in self.list_points]
        list_coords_y = [y for x, y in self.list_points]

        x_min, x_max = min(list_coords_x), max(list_coords_x)
        y_min, y_max = min(list_coords_y), max(list_coords_y)

        plt.plot(list_coords_x, list_coords_y, linewidth=LINE_WIDTH)
        plt.show()

    def test(self, display_mode_activated: bool, maximum_moves: int, tries=NB_TRIES):
        """
        Runs tests with the self avoiding walks.
        :param display_mode_activated: True to display the SAW.
        :param tries: number of tries.
        :param maximum_moves: maximum amount of moves.
        :return: None
        """

        attempt = 0
        density = []

        while attempt < tries:
            self.clear()
            moves = 0
            ariadne = []

            while moves < maximum_moves:
                for i in range(len(ariadne)):
                    if self.map[ariadne[i][0]][ariadne[i][1]] == 1:
                        ariadne.pop(i)
                        break
                for i in range(len(ariadne)):
                    escape = False
                    for j in range(len(ariadne)):
                        if ariadne[i][0] == ariadne[j][0] and ariadne[i][1] == ariadne[j][1] and j != i:
                            ariadne = ariadne[:i] + ariadne[j:]
                            escape = True
                            break
                    if escape:
                        break
                print(moves)
                infinity = self.see_infinity(self.pos)
                if len(infinity) > 2:
                    list_possibilities = self.get_possibilities(self.pos)
                    self.orientation = random.choice(list_possibilities)
                    self.move()
                    moves += 1
                elif len(infinity) == 2 or len(infinity) == 1:
                    decided = False
                    list_possibilities = self.get_possibilities(self.pos)
                    while not decided:
                        chosen = random.choice(list_possibilities)

                        if chosen in infinity:
                            self.orientation = chosen
                            decided = True
                        else:
                            line1, column1 = DIC_ORIENTATION_COORDINATES[chosen][:2]
                            line2, column2 = DIC_ORIENTATION_COORDINATES[infinity[0]][:2]
                            path = self.pathfinding([self.pos[0] + line1, self.pos[1] + column1],
                                                    [self.pos[0] + line2, self.pos[1] + column2])
                            if path is None:
                                list_possibilities.remove(chosen)
                                continue
                            self.orientation = chosen
                            ariadne = path + [np.array([self.pos[0] + line2, self.pos[1] + column2])]
                            decided = True
                    self.move()
                    moves += 1
                elif len(infinity) == 0:
                    decided = False
                    list_possibilities = self.get_possibilities(self.pos)
                    while not decided:
                        chosen = random.choice(list_possibilities)
                        line1, column1 = DIC_ORIENTATION_COORDINATES[chosen][:2]
                        for i in range(len(ariadne)):
                            if self.pos[0] + line1 == ariadne[i][0] and self.pos[1] + column1 == ariadne[i][1]:
                                ariadne = ariadne[i + 1:]
                                self.orientation = chosen
                                decided = True
                                break
                        if decided:
                            break
                        path = self.pathfinding([self.pos[0] + line1, self.pos[1] + column1], ariadne[0])
                        if path is None:
                            list_possibilities.remove(chosen)
                            continue
                        self.orientation = chosen
                        ariadne = path + ariadne
                        decided = True
                    self.move()
                    moves += 1
                if self.pos[0] == 2 or self.pos[0] == np.shape(self.map)[0] - 3:
                    self.expand()
                elif self.pos[1] == 2 or self.pos[1] == np.shape(self.map)[1] - 3:
                    self.expand()
            self.display_saw(moves)

            density.append(np.sum(self.map) / np.size(self.map))

            attempt += 1

        density = np.array(density)
        average_density = np.sum(density) / np.size(density)
        return


if __name__ == "__main__":
    """for size in range(2, 256):
        plan = Grid(size, False)
        plan.test(NB_TRIES, MAXIMUM_MOVES)
        print(f"{255 - size} left")"""
    plan = Grid(2000)
    plan.test(True, 100000)

