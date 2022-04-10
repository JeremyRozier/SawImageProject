import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from decorators import store_time, dic_function_time
import time
import numpy as np


class Ariane:
    def __init__(self, moves, display, save):
        self.moves = moves
        self.actual_move = 0
        self.display = display
        self.save = save
        self.map = {0: {0: -1}}
        self.x = 0
        self.y = 0
        self.list_x = [0]
        self.list_y = [0]
        self.minmax_x = {0: [0, 0]}
        self.minmax_y = {0: [0, 0]}
        self.total_minmax_x = [0, 0]
        self.total_minmax_y = [0, 0]
        self.orientation = random.choice(["N", "S", "E", "W"])
        self.ariadne_coord = []
        self.ariadne_side = None
        self.biases = [0.25, 0.25, 0.25, 0.25]

        self.dic_orientation_coordinates = {"N": (-1, 0),
                                            "S": (1, 0),
                                            "E": (0, 1),
                                            "W": (0, -1)}
        self.dic_side_orientations = {"right": {"N": "E",
                                                "S": "W",
                                                "E": "S",
                                                "W": "N"},
                                      "left": {"N": "W",
                                               "S": "E",
                                               "E": "N",
                                               "W": "S"}}
        self.dic_orientation_side = {"N": {"E": "left",
                                           "W": "right"},
                                     "S": {"E": "right",
                                           "W": "left"},
                                     "E": {"N": "right",
                                           "S": "left"},
                                     "W": {"N": "left",
                                           "S": "right"}}

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.step = 0
        self.result = None

    @store_time
    def ever_used(self, coord):
        try:
            _ = self.map[coord[0]][coord[1]]
            return True
        except KeyError:
            return False

    @store_time
    def probabilities(self, directions):
        same = self.biases[0] == self.biases[1] == self.biases[2] == self.biases[3]
        if len(directions) > 1 and not same:
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
        for direction in ["N", "S", "E", "W"]:
            line, column = self.dic_orientation_coordinates[direction]
            if self.ever_used([self.y + line, self.x + column]):
                if self.map[self.y + line][self.x + column] != -1:
                    directions.append(direction)
            else:
                directions.append(direction)
        return directions

    @store_time
    def see_infinity(self):
        directions = []
        if self.y == self.minmax_y[self.x][0]:
            directions.append("N")
        if self.y == self.minmax_y[self.x][1]:
            directions.append("S")
        if self.x == self.minmax_x[self.y][1]:
            directions.append("E")
        if self.x == self.minmax_x[self.y][0]:
            directions.append("W")
        return directions

    @store_time
    def update_side(self):
        opposite = {"right": "left", "left": "right"}
        to_ariadne = self.dic_side_orientations[opposite[self.ariadne_side]][self.orientation]
        line, column = self.dic_orientation_coordinates[to_ariadne]
        coord = [self.y + line, self.x + column]
        if self.ever_used(coord):
            if self.map[coord[0]][coord[1]] > 0:
                self.ariadne_side = opposite[self.ariadne_side]

    @store_time
    def remove_possibilities(self, possibilities):
        if self.ariadne_side is not None:
            self.update_side()
        line1, column1 = self.dic_orientation_coordinates[self.orientation]
        coord = [self.y + line1, self.x + column1]
        if self.ever_used(coord):
            if self.map[coord[0]][coord[1]] > 0:
                sidestep = self.dic_side_orientations["left"][self.orientation]
                line2, column2 = self.dic_orientation_coordinates[sidestep]
                coord1 = [self.y + line1 + line2, self.x + column1 + column2]
                coord2 = [self.y + line1 - line2, self.x + column1 - column2]
                if self.ever_used(coord1):
                    if self.map[coord1[0]][coord1[1]] == -1:
                        to_remove = sidestep
                        while to_remove in possibilities:
                            possibilities.remove(to_remove)
                if self.ever_used(coord2):
                    if self.map[coord2[0]][coord2[1]] == -1:
                        to_remove = self.dic_side_orientations["right"][self.orientation]
                        while to_remove in possibilities:
                            possibilities.remove(to_remove)
        if self.ariadne_side is not None:
            line1, column1 = self.dic_orientation_coordinates[self.orientation]
            to_ariadne = self.dic_side_orientations[self.ariadne_side][self.orientation]
            line2, column2 = self.dic_orientation_coordinates[to_ariadne]
            coord1 = [self.y + line1 - line2, self.x + column1 - column2]
            opposite = {"right": "left", "left": "right"}
            if self.ever_used(coord1):
                if self.map[coord1[0]][coord1[1]] == -1:
                    to_remove = self.dic_side_orientations[opposite[self.ariadne_side]][self.orientation]
                    while to_remove in possibilities:
                        possibilities.remove(to_remove)
            coord2 = [self.y + line1 + line2, self.x + column1 + column2]
            if self.ever_used(coord2):
                if self.map[coord2[0]][coord2[1]] == -1:
                    to_remove1 = self.orientation
                    to_remove2 = self.dic_side_orientations[opposite[self.ariadne_side]][self.orientation]
                    while to_remove1 in possibilities:
                        possibilities.remove(to_remove1)
                    while to_remove2 in possibilities:
                        possibilities.remove(to_remove2)
        return possibilities

    @store_time
    def clear_ariadne(self, to):
        if to > 0:
            to -= 1
        if to < len(self.ariadne_coord):
            for coord in self.ariadne_coord[to:]:
                if self.map[coord[0]][coord[1]] != -1:
                    self.map[coord[0]][coord[1]] = 0
            if to == 0:
                self.ariadne_coord = []
            else:
                self.ariadne_coord = self.ariadne_coord[:to]

    @store_time
    def anchor_ariadne(self, chosen):
        self.clear_ariadne(0)
        line, column = self.dic_orientation_coordinates[chosen]
        self.ariadne_side = None
        if chosen == "N":
            boucle = abs(self.total_minmax_y[0] - self.y)
        elif chosen == "S":
            boucle = abs(self.total_minmax_y[1] - self.y)
        elif chosen == "E":
            boucle = abs(self.total_minmax_x[1] - self.x)
        else:
            boucle = abs(self.total_minmax_x[0] - self.x)
        if boucle > 25:
            boucle = 25
        while boucle >= 2:
            coord = [self.y + line * boucle, self.x + column * boucle]
            if coord[0] in self.map.keys():
                self.map[coord[0]].update({coord[1]: len(self.ariadne_coord) + 1})
            else:
                self.map.update({coord[0]: {coord[1]: len(self.ariadne_coord) + 1}})
            self.ariadne_coord.append(coord)
            boucle -= 1

    @store_time
    def look_for_ariadne(self, chosen):
        line, column = self.dic_orientation_coordinates[chosen]
        coord1 = [self.y + line - 1, self.x + column]
        coord2 = [self.y + line + 1, self.x + column]
        coord3 = [self.y + line, self.x + column + 1]
        coord4 = [self.y + line, self.x + column - 1]
        coordinates = [coord1, coord2, coord3, coord4]
        minimum = None
        for i in range(4):
            if self.ever_used(coordinates[i]):
                tile_value = self.map[coordinates[i][0]][coordinates[i][1]]
                if tile_value > 0:
                    if minimum is not None:
                        if tile_value < minimum:
                            minimum = tile_value
                    else:
                        minimum = tile_value
        if minimum is not None:
            self.clear_ariadne(minimum + 1)
            return True
        return False

    @store_time
    def go_on_ariadne(self):
        coord1 = [self.y - 1, self.x]
        coord2 = [self.y + 1, self.x]
        coord3 = [self.y, self.x + 1]
        coord4 = [self.y, self.x - 1]
        coordinates = [coord1, coord2, coord3, coord4]
        minimum = None
        index = None
        for i in range(4):
            if self.ever_used(coordinates[i]):
                tile_value = self.map[coordinates[i][0]][coordinates[i][1]]
                if tile_value > 0:
                    if minimum is not None:
                        if tile_value < minimum:
                            minimum = tile_value
                            index = i
                    else:
                        minimum = tile_value
                        index = i
        if minimum is not None:
            self.clear_ariadne(minimum)
            directions = ["N", "S", "E", "W"]
            to_ariadne = directions[index]
            return to_ariadne
        return None

    @store_time
    def ariadne_line(self):
        line1, column1 = self.dic_orientation_coordinates[self.orientation]
        to_ariadne = self.dic_side_orientations[self.ariadne_side][self.orientation]
        line2, column2 = self.dic_orientation_coordinates[to_ariadne]
        coord = [self.y + line1 + line2, self.x + column1 + column2]
        if self.ever_used(coord):
            tile_value = self.map[coord[0]][coord[1]]
            if tile_value > 0:
                self.clear_ariadne(tile_value + 1)
            else:
                self.map[coord[0]][coord[1]] = len(self.ariadne_coord) + 1
                self.ariadne_coord.append(coord)
        else:
            if coord[0] in self.map.keys():
                self.map[coord[0]].update({coord[1]: len(self.ariadne_coord) + 1})
            else:
                self.map.update({coord[0]: {coord[1]: len(self.ariadne_coord) + 1}})
            self.ariadne_coord.append(coord)

    @store_time
    def ariadne_turn(self, chosen):
        line1, column1 = self.dic_orientation_coordinates[self.orientation]
        line2, column2 = self.dic_orientation_coordinates[chosen]
        coord1 = [self.y + line1 - line2, self.x + column1 - column2]
        coord2 = [self.y + line1, self.x + column1]
        coord3 = [self.y + line1 + line2, self.x + column1 + column2]
        coordinates = [coord1, coord2, coord3]
        for coord in coordinates:
            if self.ever_used(coord):
                tile_value = self.map[coord[0]][coord[1]]
                if tile_value > 0:
                    self.clear_ariadne(tile_value + 1)
                elif tile_value == -1:
                    continue
                else:
                    self.map[coord[0]][coord[1]] = len(self.ariadne_coord) + 1
                    self.ariadne_coord.append(coord)
            else:
                if coord[0] in self.map.keys():
                    self.map[coord[0]].update({coord[1]: len(self.ariadne_coord) + 1})
                else:
                    self.map.update({coord[0]: {coord[1]: len(self.ariadne_coord) + 1}})
                self.ariadne_coord.append(coord)

    @store_time
    def handle_ariadne(self, chosen):
        if chosen == self.orientation:
            self.ariadne_line()
        else:
            self.ariadne_turn(chosen)

    def make_decision(self, possibilities, infinity):
        while True:
            if len(possibilities) > 0:
                chosen = random.choice(possibilities)
                if chosen in infinity:
                    self.anchor_ariadne(chosen)
                    return chosen
                if self.ariadne_side is None:
                    self.ariadne_side = self.dic_orientation_side[self.orientation][chosen]
                line, column = self.dic_orientation_coordinates[chosen]
                coord = [self.y + line, self.x + column]
                if self.ever_used(coord):
                    tile_value = self.map[coord[0]][coord[1]]
                    if tile_value > 0:
                        self.clear_ariadne(tile_value)
                        return chosen
                found_ariadne = self.look_for_ariadne(chosen)
                if found_ariadne:
                    return chosen
                self.handle_ariadne(chosen)
                return chosen
            else:
                to_ariadne = self.go_on_ariadne()
                if to_ariadne is not None:
                    return to_ariadne
                else:
                    self = Ariane(self.moves, self.display, self.save)
                    t1 = time.time()
                    self.run()
                    print(f"the whole program took {time.time() - t1} seconds.")
                    for function, list_seconds in dic_function_time.items():
                        print(f"Time took by {function} : {sum(list_seconds)} seconds.")
                    self.display_saw()
                    quit()

    @store_time
    def move(self):
        line, column = self.dic_orientation_coordinates[self.orientation]
        self.y += line
        self.x += column
        self.list_y.append(-self.y)
        self.list_x.append(self.x)
        if self.x in self.minmax_y.keys():
            if self.y < self.minmax_y[self.x][0]:
                self.minmax_y[self.x][0] = self.y
            elif self.y > self.minmax_y[self.x][1]:
                self.minmax_y[self.x][1] = self.y
        else:
            self.minmax_y.update({self.x: [self.y, self.y]})
        if self.y in self.minmax_x.keys():
            if self.x < self.minmax_x[self.y][0]:
                self.minmax_x[self.y][0] = self.x
            elif self.x > self.minmax_x[self.y][1]:
                self.minmax_x[self.y][1] = self.x
        else:
            self.minmax_x.update({self.y: [self.x, self.x]})
        if self.y in self.map.keys():
            self.map[self.y].update({self.x: -1})
        else:
            self.map.update({self.y: {self.x: -1}})
        if self.x < self.total_minmax_x[0]:
            self.total_minmax_x[0] = self.x
        if self.x > self.total_minmax_x[1]:
            self.total_minmax_x[1] = self.x
        if self.y < self.total_minmax_y[0]:
            self.total_minmax_y[0] = self.y
        if self.y > self.total_minmax_y[1]:
            self.total_minmax_y[1] = self.y

    def animate(self, i):
        self.ax.plot(self.list_x[(i - 1) * self.step - 1:i * self.step],
                     self.list_y[(i - 1) * self.step - 1:i * self.step],
                     c='black', linewidth=0.5)

    def display_saw(self):
        self.step = (self.moves // 455) + 1
        if self.display:
            anim1 = animation.FuncAnimation(self.fig, self.animate, interval=33)
            plt.show()
            self.ax.clear()
        if self.save:
            anim2 = animation.FuncAnimation(self.fig, self.animate, interval=33, frames=455)
            anim2.save("pictures/saw_animation.gif", writer="ffmpeg")

    def step_forward(self):
        print(self.actual_move, "({}%)".format(round(self.actual_move / self.moves * 100)))
        possibilities = self.get_possibilities()
        possibilities = self.probabilities(possibilities)
        if self.actual_move == 0:
            possibilities = self.orientation
        possibilities = self.remove_possibilities(possibilities)
        infinity = self.see_infinity()
        self.orientation = self.make_decision(possibilities, infinity)
        self.move()
        self.actual_move += 1

    def run(self):
        while self.actual_move < self.moves:
            self.step_forward()


class WithPicture:
    def __init__(self, picture, display, save):
        self.picture = picture
        pic_size = np.shape(self.picture)
        self.density_map = np.zeros(pic_size)
        self.SAW_workspace_range = [pic_size[0] * 16, pic_size[1] * 16]
        self.SAW_workspace = [[-self.SAW_workspace_range[0] // 2, self.SAW_workspace_range[0] // 2],
                              [-self.SAW_workspace_range[1] // 2, self.SAW_workspace_range[1] // 2]]
        self.density_weight = 0.05
        self.workspace_weight = 0.001
        self.bias1 = [0.0, 0.0, 0.0, 0.0]
        self.bias2 = [0.0, 0.0, 0.0, 0.0]
        self.bias3 = [0.0, 0.0, 0.0, 0.0]
        self.total = 0
        for i in range(np.shape(self.picture)[0]):
            for j in range(np.shape(self.picture)[1]):
                self.total += self.picture[i][j]
        self.total = int(self.total)
        self.SAW = Ariane(self.total, display, save)

    def workspace_bias(self):
        bias = [0.0, 0.0, 0.0, 0.0]
        if self.SAW.y < self.SAW_workspace[0][0]:
            bias_value = min(0.25, abs(self.SAW.y - self.SAW_workspace[0][0]) * self.workspace_weight)
            bias[1] += bias_value
            bias[0] -= bias_value
        elif self.SAW.y > self.SAW_workspace[0][1]:
            bias_value = min(0.25, abs(self.SAW.y - self.SAW_workspace[0][1]) * self.workspace_weight)
            bias[1] -= bias_value
            bias[0] += bias_value
        if self.SAW.x < self.SAW_workspace[1][0]:
            bias_value = min(0.25, abs(self.SAW.x - self.SAW_workspace[1][0]) * self.workspace_weight)
            bias[2] += bias_value
            bias[3] -= bias_value
        elif self.SAW.x > self.SAW_workspace[1][1]:
            bias_value = min(0.25, abs(self.SAW.x - self.SAW_workspace[1][1]) * self.workspace_weight)
            bias[2] -= bias_value
            bias[3] += bias_value
        return bias

    def get_pixel(self):
        y_pixel = self.SAW.y / 16 + 8 * np.shape(self.picture)[0]
        x_pixel = self.SAW.x / 16 + 8 * np.shape(self.picture)[1]
        y_result = None
        x_result = None
        for i in range(max(np.shape(self.picture))):
            if i * 16 <= y_pixel < (i + 1) * 16:
                y_result = i
            if i * 16 <= x_pixel < (i + 1) * 16:
                x_result = i
        return [y_result, x_result]

    def pixel_bias(self):
        bias = [0.0, 0.0, 0.0, 0.0]
        y_pixel, x_pixel = self.get_pixel()
        if y_pixel is not None and x_pixel is not None:
            if self.picture[y_pixel][x_pixel] - self.density_map[y_pixel][x_pixel] > 16:
                center = [[16 * y_pixel + 7, 16 * y_pixel + 8], [16 * x_pixel + 7, 16 * x_pixel + 8]]
                diff_y1 = center[0][0] - self.SAW.y
                diff_y2 = self.SAW.y - center[0][1]
                if diff_y1 > 0:
                    bias_value = min(0.25, self.density_weight * diff_y1)
                    bias[0] -= bias_value
                    bias[1] += bias_value
                elif diff_y2 > 0:
                    bias_value = min(0.25, self.density_weight * diff_y2)
                    bias[0] += bias_value
                    bias[1] -= bias_value
                diff_x1 = center[1][0] - self.SAW.x
                diff_x2 = self.SAW.x - center[1][1]
                if diff_x1 > 0:
                    bias_value = min(0.25, self.density_weight * diff_x1)
                    bias[2] += bias_value
                    bias[3] -= bias_value
                elif diff_x2 > 0:
                    bias_value = min(0.25, self.density_weight * diff_x2)
                    bias[2] -= bias_value
                    bias[3] += bias_value
        return bias

    def gravitational_bias(self):
        bias = [0.0, 0.0, 0.0, 0.0]
        if self.bias1 == [0.0, 0.0, 0.0, 0.0] and self.bias2 == [0.0, 0.0, 0.0, 0.0]:
            y_pixel, x_pixel = self.get_pixel()
            if y_pixel is not None and x_pixel is not None:
                diff = self.picture - self.density_map
                total = np.array([0, 0, 0, 0])
                for i in range(np.shape(diff)[0]):
                    for j in range(np.shape(diff)[1]):
                        if i < y_pixel:
                            total[0] += diff[i][j]
                        elif i > y_pixel:
                            total[1] += diff[i][j]
                        if j < x_pixel:
                            total[3] += diff[i][j]
                        elif j > x_pixel:
                            total[2] += diff[i][j]
                maximum = np.nanmax(total)
                if maximum != 0:
                    bias = total / (maximum * 2)
                    bias = bias - np.array([0.25, 0.25, 0.25, 0.25])
                    bias = np.nan_to_num(bias)
                    bias = bias.tolist()
        return bias

    def update_density(self):
        y_pixel, x_pixel = self.get_pixel()
        if y_pixel is not None and x_pixel is not None:
            self.density_map[y_pixel][x_pixel] += 1

    def display_saw(self):
        self.SAW.display_saw()

    def run(self):
        move = 0
        while move < self.total:
            self.bias1 = self.workspace_bias()
            self.bias2 = self.pixel_bias()
            #self.bias3 = self.gravitational_bias()
            new_bias = [0.25, 0.25, 0.25, 0.25]
            for i in range(4):
                new_bias[i] += self.bias1[i]
                new_bias[i] += self.bias2[i]
                #new_bias[i] += self.bias3[i]
            self.SAW.biases = new_bias
            self.SAW.step_forward()
            self.update_density()
            move += 1
        self.SAW.display_saw()


"""plan = Ariane(10000, True, False)
t1 = time.time()
plan.run()
print(f"the whole program took {time.time() - t1} seconds.")
for function, list_seconds in dic_function_time.items():
    print(f"Time took by {function} : {sum(list_seconds)} seconds.")
plan.display_saw()"""
