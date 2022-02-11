import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from constants import DIC_DATA, DATA_FILENAME


class Statistics:
    """Static class which handles data operations."""

    @staticmethod
    def save(**data_arguments):
        """
        Overwrites the data contained in 'data_filename' and saves 'dic_to_save' :
        - size (int) : size of the grid related to the data we wanna save.
        - dic_to_save (dict) : {size: {'average_moves': [], 'density': [], 'max': [], 'min': []}}.
        - data_filename (str) : file's path where to serialize 'dic_to_save.'

        If the file doesn't exist, then it will create the file and store DIC_DATA.
        Be careful, whatever happens it will overwrite the file's content first.
        """
        if "size" not in data_arguments:
            print("Please specify the size of the grid related to the data.")
            return

        if "dic_to_save" not in data_arguments:
            print("Please specify the dic to save.")
            return

        if "data_filename" not in data_arguments:
            print("Please specify the file where to save the data.")
            return

        size = data_arguments["size"]
        dic_to_save = data_arguments["dic_to_save"]
        data_filename = data_arguments["data_filename"]

        if not os.path.isfile(data_filename):
            with open(data_filename, 'wb') as file:
                pickle.dump(DIC_DATA, file)

        new_dic = DIC_DATA
        for data_type, values in dic_to_save.items():
            new_dic[size][data_type].append((np.sum(values)/np.size(values)).tolist())

        with open(data_filename, 'wb') as file:
            pickle.dump(new_dic, file)

    @staticmethod
    def display(data_filename):
        """
        Displays the data contained in 'dic_to_save' in 'data_filename' :
         - data_filename (str) : file's path where to serialize 'dic_to_save'.
         - required format : dic_to_save (dict) : {size: {'average_moves': [],
        'average_density': [], 'max_moves': [], 'min_moves': []}}.
         """
        with open(data_filename, 'rb') as file:
            dic_size_data = pickle.load(file)

        fig, axs = plt.subplots(2, 2)
        ((ax1, ax2), (ax3, ax4)) = axs

        list_sizes = []
        list_average_moves = []
        list_density = []
        list_max = []
        list_min = []
        nb_sizes = len(dic_size_data)

        for size, dic_data in dic_size_data.items():
            list_sizes.append(size)
            average_moves = dic_data["average_moves"]
            density = dic_data["average_density"]
            max_moves = dic_data["max_moves"]
            min_moves = dic_data["min_moves"]

            list_average_moves += average_moves
            list_density += density
            list_max += max_moves
            list_min += min_moves

            if nb_sizes == size:
                break

        ax1.plot(list_sizes, list_average_moves, label="Average moves")
        ax1.set_xlabel("size")
        ax1.legend()

        ax2.plot(list_sizes, list_density, label="Density")
        ax2.set_xlabel("size")
        ax2.legend()

        ax3.plot(list_sizes, list_max, label="Max movements")
        ax3.set_xlabel("size")
        ax3.legend()

        ax4.plot(list_sizes, list_min, label="Min movements")
        ax4.set_xlabel("size")
        ax4.legend()

        fig.tight_layout()
        plt.subplots_adjust()
        plt.show()


if __name__ == "__main__":
    Statistics.display(DATA_FILENAME)