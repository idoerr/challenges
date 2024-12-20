from enum import Enum

#from copy import deepcopy
def deepcopy(matrix):
    return list(map(list, matrix))

class Direction(Enum):
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3
    OFF_MAP = 4

def run_guard_path(matrix, start_row, start_col):

    row = start_row
    col = start_col
    dir = Direction.NORTH

    location_history = set()
    location_history.add((row, col, dir))

    unique_steps = 0

    iter_count = 0

    while dir != Direction.OFF_MAP and iter_count < 500000:
        iter_count += 1
        row, col, dir, is_unique = take_step(matrix, row, col, dir)

        if (row, col, dir) in location_history:
            return True
        location_history.add((row, col, dir))
        
    return False
        
        
def take_step(matrix, row, col, move_dir):

    is_unique = matrix[row][col] != 'X'
    matrix[row][col] = 'X'

    next_row = row
    next_col = col
    next_dir = move_dir

    match move_dir:
        case Direction.NORTH:
            if row-1 < 0:
                next_dir = Direction.OFF_MAP
                return (row, col, next_dir, is_unique)
            
            if matrix[row-1][col] != '#':
                next_row = row-1
            else:
                next_dir = Direction.EAST
            
        case Direction.EAST:
            if col+1 >= len(matrix[0]):
                next_dir = Direction.OFF_MAP
                return (row, col, next_dir, is_unique)
            
            if matrix[row][col+1] != '#':
                next_col = col+1
            else:
                next_dir = Direction.SOUTH
        
        case Direction.WEST:
            if col-1 < 0:
                next_dir = Direction.OFF_MAP
                return (row, col, next_dir, is_unique)
            
            if matrix[row][col-1] != '#':
                next_col = col-1
            else:
                next_dir = Direction.NORTH

        case Direction.SOUTH:
            if row+1 >= len(matrix):
                next_dir = Direction.OFF_MAP
                return (row, col, next_dir, is_unique)
            
            if matrix[row+1][col] != '#':
                next_row = row+1
            else:
                next_dir = Direction.WEST
    
    return (next_row, next_col, next_dir, is_unique)

if __name__ == "__main__":
    file_name = 'adventofcode2024/day6puz1input.txt'

    data_matrix = []
    start_row = -1
    start_col = -1

    row = 0
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(list(line.strip()))

            # find the starting position of the 
            col = line.find('^')
            if col != -1:
                start_row = row
                start_col = col
            row += 1

    first_run_matrix = deepcopy(data_matrix)

    # run the guard path the first time
    run_guard_path(first_run_matrix, start_row, start_col)

    def pretty_print_matrix(matrix):
        for row in matrix:
            print(''.join(row))

    #pretty_print_matrix(first_run_matrix)

    print(len(first_run_matrix))

    possible_loops = 0

    for row_index, row in enumerate(first_run_matrix):
        print(row_index)
        for col_index, value in enumerate(row):
            if value == 'X' and not(row_index == start_row and col_index == start_col):
                sub_run_matrix = deepcopy(data_matrix)
                sub_run_matrix[row_index][col_index] = '#'
                is_loop = run_guard_path(sub_run_matrix, start_row, start_col)
                #is_loop = False

                sub_run_matrix[row_index][col_index] = 'O'

                if is_loop:
                    possible_loops += 1



    print()
    print(possible_loops)