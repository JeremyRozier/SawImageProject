DIC_ORIENTATION_COORDINATES = {
    # orientation : (line, column, axis)
    "N": (-1, 0, 0),
    "S": (1, 0, 0),
    "E": (0, 1, 1),
    "W": (0, -1, 1)
}

DIC_DATA = {size: {'average_moves': 0, 'average_density': 0, 'max_moves': 0, 'min_moves': 0}
            for size in range(2, 256)}

DATA_FILENAME = "data_files/stored_data.pk"
CSV_FILENAME = "data_files/data_tables.csv"

CSV_HEADER = ['size', 'average_moves', 'average_density', 'max_moves', 'min_moves']

LINE_WIDTH = 3
NB_TRIES = 1
MAXIMUM_MOVES = 10e3
