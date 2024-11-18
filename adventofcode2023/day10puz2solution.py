
from enum import Enum
from collections import deque

class Direction(Enum):
    NORTH = 0
    EAST = 1
    WEST = 2
    SOUTH = 3

def try_step_direction(map_matrix, cur_loc, direction):

    #Determine where the next step would be
    match direction:
        case Direction.NORTH:
            new_location = (cur_loc[0] - 1, cur_loc[1])
        case Direction.EAST:
            new_location = (cur_loc[0], cur_loc[1] + 1)
        case Direction.WEST:
            new_location = (cur_loc[0], cur_loc[1] - 1)
        case Direction.SOUTH:
            new_location = (cur_loc[0] + 1, cur_loc[1])

    # Test the bounds
    if new_location[0] < 0 or new_location[0] >= len(map_matrix):
        raise IndexError( 'Cannot move direction: ' + str(direction) + ', resulting coord ' + new_location )
    
    if new_location[1] < 0 or new_location[1] >= len(map_matrix[new_location[0]]):
        raise IndexError( 'Cannot move direction: ' + str(direction) + ', resulting coord ' + new_location )

    # Check to see if the pipe at the new location is valid, and set direction
    pipe_char = map_matrix[new_location[0]][new_location[1]]

    match direction:
        case Direction.NORTH:
            if pipe_char == '|' or pipe_char == 'S':
                new_direction = Direction.NORTH
            elif pipe_char == '7':
                new_direction = Direction.WEST
            elif pipe_char == 'F':
                new_direction = Direction.EAST
            else:
                raise RuntimeError('Disconnected pipe! Direction: ' + str(direction) + ', coord: ' + new_location + ', pipe: ' + pipe_char)
        case Direction.EAST:
            if pipe_char == '-' or pipe_char == 'S':
                new_direction = Direction.EAST
            elif pipe_char == '7':
                new_direction = Direction.SOUTH
            elif pipe_char == 'J':
                new_direction = Direction.NORTH
            else:
                raise RuntimeError('Disconnected pipe! Direction: ' + str(direction) + ', coord: ' + new_location + ', pipe: ' + pipe_char)
        case Direction.WEST:
            if pipe_char == '-' or pipe_char == 'S':
                new_direction = Direction.WEST
            elif pipe_char == 'F':
                new_direction = Direction.SOUTH
            elif pipe_char == 'L':
                new_direction = Direction.NORTH
            else:
                raise RuntimeError('Disconnected pipe! Direction: ' + str(direction) + ', coord: ' + new_location + ', pipe: ' + pipe_char)
        case Direction.SOUTH:
            if pipe_char == '|' or pipe_char == 'S':
                new_direction = Direction.SOUTH
            elif pipe_char == 'J':
                new_direction = Direction.WEST
            elif pipe_char == 'L':
                new_direction = Direction.EAST
            else:
                raise RuntimeError('Disconnected pipe! Direction: ' + direction + ', coord: ' + new_location + ', pipe: ' + pipe_char)
    
    return new_location, new_direction

def try_append_queue(space_matrix, space_matrix_dim, queue, check_loc):
    if check_loc[0] < 0 or check_loc[0] >= space_matrix_dim[0]:
        return
    if check_loc[1] < 0 or check_loc[1] >= space_matrix_dim[1]:
        return
    if space_matrix[check_loc[0]][check_loc[1]] == 0:
        queue.append(check_loc)

def do_mark_loc(space_matrix, space_matrix_dim, queue, cur_loc):
    space_matrix[cur_loc[0]][cur_loc[1]] = 2

    try_append_queue(space_matrix, space_matrix_dim, queue, (cur_loc[0] + 1, cur_loc[1]))
    try_append_queue(space_matrix, space_matrix_dim, queue, (cur_loc[0] - 1, cur_loc[1]))
    try_append_queue(space_matrix, space_matrix_dim, queue, (cur_loc[0], cur_loc[1] + 1))
    try_append_queue(space_matrix, space_matrix_dim, queue, (cur_loc[0], cur_loc[1] - 1))

# Convert the string matrix into an int matrix, where every character becomes a 3x3 grid, with pipe segments blocking accordingly.
# We will then use a coloring algorithm to find which cells have outside access.  0 means empty spot 1 means blocked, 2 means visited.
# S: 010 |: 010 -: 000 L: 010 F: 000 J: 010  7: 000  Else: 000
#    111    010    111    011    011    110     110        000
#    010    010    000    000    010    000     010        000
def convert_map_to_space_matrix(map_matrix, travel_path):
    space_matrix = []
    for row_num, row in enumerate(map_matrix):
        top_row = []
        mid_row = []
        bot_row = []

        for col_num, x in enumerate(row):
            if not ((row_num, col_num) in travel_path):
                top_row.extend([0, 0, 0])
                mid_row.extend([0, 0, 0])
                bot_row.extend([0, 0, 0])
                continue
            match x:
                case 'S':
                    top_row.extend([0, 1, 0])
                    mid_row.extend([1, 1, 1])
                    bot_row.extend([0, 1, 0])
                case '|':
                    top_row.extend([0, 1, 0])
                    mid_row.extend([0, 1, 0])
                    bot_row.extend([0, 1, 0])
                case '-':
                    top_row.extend([0, 0, 0])
                    mid_row.extend([1, 1, 1])
                    bot_row.extend([0, 0, 0])
                case 'L':
                    top_row.extend([0, 1, 0])
                    mid_row.extend([0, 1, 1])
                    bot_row.extend([0, 0, 0])
                case 'F':
                    top_row.extend([0, 0, 0])
                    mid_row.extend([0, 1, 1])
                    bot_row.extend([0, 1, 0])
                case 'J':
                    top_row.extend([0, 1, 0])
                    mid_row.extend([1, 1, 0])
                    bot_row.extend([0, 0, 0])
                case '7':
                    top_row.extend([0, 0, 0])
                    mid_row.extend([1, 1, 0])
                    bot_row.extend([0, 1, 0])
                case _:
                    top_row.extend([0, 0, 0])
                    mid_row.extend([0, 0, 0])
                    bot_row.extend([0, 0, 0])
        
        space_matrix.append(top_row)
        space_matrix.append(mid_row)
        space_matrix.append(bot_row)
    return space_matrix

if __name__ == "__main__":
    file_name = 'adventofcode2023/day10puz2input.txt'

    s_loc = None
    map_matrix = []

    #load in the map matrix, and find the start position
    with open(file_name, 'r') as file_handle:
        for row in file_handle:
            s_index = row.find('S')
            if s_index != -1:
                s_loc = (len(map_matrix), row.find('S'))

            map_matrix.append(row.strip())

    cur_loc = s_loc

    travel_path = [cur_loc]
    cur_direction = None

    # try to make steps until one is valid.
    test_dirs = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
    for test_direction in test_dirs:

        try:
            cur_loc, cur_direction = try_step_direction(map_matrix, cur_loc, test_direction)
            travel_path.append(cur_loc)
            break
        except:
            pass

    # Take steps until we end up at the beginning again.  Keep track of path along the way.
    while cur_loc != s_loc:
        cur_loc, cur_direction = try_step_direction(map_matrix, cur_loc, cur_direction)
        travel_path.append(cur_loc)

    space_matrix = convert_map_to_space_matrix(map_matrix, travel_path)
    space_matrix_dim = (len(space_matrix), len(space_matrix[0]))

    # for row in space_matrix:
    #     cur_row = ''
    #     for col in row:
    #         cur_row += str(col)
    #     print(cur_row)

    # Add the outside edges to the check queue
    check_queue = deque()

    # Left and right columns
    for row in range(0, space_matrix_dim[0]):
        left_col = 0
        right_col = space_matrix_dim[1] - 1

        check_loc = (row, left_col)
        try_append_queue(space_matrix, space_matrix_dim, check_queue, check_loc)

        check_loc = (row, right_col)
        try_append_queue(space_matrix, space_matrix_dim, check_queue, check_loc)

    # Top and bottom rows
    for col in range(0, space_matrix_dim[1]):
        top_row = 0
        bot_row = space_matrix_dim[0]

        check_loc = (top_row, col)
        try_append_queue(space_matrix, space_matrix_dim, check_queue, check_loc)

        check_loc = (bot_row, col)
        try_append_queue(space_matrix, space_matrix_dim, check_queue, check_loc)

    # Now visit nodes, and mark adjacent nodes for subsequent visiting.
    while(len(check_queue) > 0):
        cur_loc = check_queue.pop()

        do_mark_loc(space_matrix, space_matrix_dim, check_queue, cur_loc)

    enclosed_cells = []
    # Determine which cells are blocked in by using the middle cell in each 3x3 block.
    # If it is still 0 after the visiting algo has passed, then it is enclosed.
    for map_row in range(len(map_matrix)):
        space_row = 1 + map_row * 3
        for map_col in range(len(map_matrix[0])):
            space_col = 1 + map_col * 3
            if space_matrix[space_row][space_col] == 0:
                enclosed_cells.append((map_row, map_col))
    
    #Make a pretty-print version of the map matrix
    output_map = []
    for map_row in range(len(map_matrix)):
        output_map.append(['O'] * len(map_matrix[0]))

    for map_row, map_col in travel_path:
        output_map[map_row][map_col] = map_matrix[map_row][map_col]

    for map_row, map_col in enclosed_cells:
        output_map[map_row][map_col] = 'I'

    # print('k')
    # for row in output_map:
    #     cur_row = ''
    #     for col in row:
    #         cur_row += col
    #     print(cur_row)
    
    
    print(s_loc)
    print(len(travel_path) / 2)
    print(len(enclosed_cells))

