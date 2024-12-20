from enum import Enum

class Direction(Enum):
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3
    OFF_MAP = 4

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

    data_matrix = [];
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

    row = start_row
    col = start_col
    dir = Direction.NORTH

    unique_steps = 0

    iter_count = 0

    while dir != Direction.OFF_MAP and iter_count < 500000:
        iter_count += 1
        row, col, dir, is_unique = take_step(data_matrix, row, col, dir)

        if is_unique:
            unique_steps += 1

    print()
    print(unique_steps)
    
    
