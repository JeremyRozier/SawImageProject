DIC_ORIENTATION_COORDINATES = {
    # orientation : (line, column, axis)
    "N": (-1, 0, 0),
    "S": (1, 0, 0),
    "E": (0, 1, 1),
    "W": (0, -1, 1)
}

DIC_DATA = {size: {'average_moves': [], 'average_density': [], 'max_moves': [], 'min_moves': []}
            for size in range(2, 256)}
DATA_FILENAME = "stored_data.pk"
NB_TRIES = 10e3
MAXIMUM_MOVES = 10e3
