import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from constants import DIC_DATA, DATA_FILENAME, CSV_FILENAME, CSV_HEADER
import csv


class Statistics:
    """Static class which handles data operations."""

    @staticmethod
    def save(**data_arguments):
        """
        - Saves the considered dictionary in the chosen file.
        - If the file doesn't exist, then it will create the file and store DIC_DATA.
        - Warning: Be careful, whatever happens it will overwrite the file's content first.

        :param data_arguments:
            - size (int) : size of the grid related to the data we wanna save.
            - dic_to_save (dict) : {size: {'average_moves': [], 'density': [], 'max': [], 'min': []}}.
            - data_filename (str) : file's path where to serialize 'dic_to_save.'

        :return: None
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

        new_dic = DIC_DATA
        for data_type, values in dic_to_save.items():
            new_dic[size][data_type].append((np.sum(values) / np.size(values))[0])

        with open(data_filename, 'wb') as file:
            pickle.dump(new_dic, file)

    @staticmethod
    def save_to_csv(data_filename=DATA_FILENAME, csv_filename=CSV_FILENAME):
        """
        - Creates a csv file by reading with the dictionary stored in the file.
        - If the file doesn't exist, then it will create the file and store DIC_DATA.
        - Warning: Be careful, if the csv file exists, whatever happens, it will overwrite the csv content first.

        :param data_filename: file's path where to get 'dic_size_statistics'.required format dic_to_save (dict) : {
        size: {'average_moves': [],average_density' [], 'max_moves': [], 'min_moves': []}}.

        :param csv_filename: file's path where to write 'dic_size_statistics'.

        :return: None

        """

        if not os.path.isfile(data_filename):
            print(f"{data_filename} doesn't exist")
            return

        with open(data_filename, 'rb') as data_file:
            dic_size_statistics = pickle.load(data_file)

        with open(csv_filename, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(CSV_HEADER)

            for size, dic_statistics in dic_size_statistics.items():
                list_current_values = [size]

                for statistic_name, statistic_value in dic_statistics.items():
                    list_current_values.append(statistic_value[0])
                writer.writerow(list_current_values)

    @staticmethod
    def display(data_filename):
        """
        - Displays the data contained in 'dic_to_save' in 'data_filename'.

        :param data_filename:
            - data_filename (str) : file's path where to serialize 'dic_to_save'.
            - required format : dic_to_save (dict) : {size: {'average_moves': [],
            'average_density': [], 'max_moves': [], 'min_moves': []}}.

        :return: None
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

            list_average_moves.append(average_moves)
            list_density.append(density)
            list_max.append(max_moves)
            list_min.append(min_moves)

            # To make sure list_sizes and other lists have same length for plots
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
