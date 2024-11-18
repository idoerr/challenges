
from enum import Enum

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
        
    

if __name__ == "__main__":
    file_name = 'adventofcode2023/day10puz1input.txt'

    s_loc = None
    map_matrix = []

    #load in the map matrix, and find the start position
    with open(file_name, 'r') as file_handle:
        for row in file_handle:
            s_index = row.find('S')
            if s_index != -1:
                s_loc = (len(map_matrix), row.find('S'))

            map_matrix.append(row)

    cur_loc = s_loc

    travel_path = [cur_loc]
    cur_direction = None

    # try to make steps until one is valid.
    test_dirs = [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]
    for test_direction in test_dirs:

        try:
            cur_loc, cur_direction = try_step_direction(map_matrix, cur_loc, test_direction)
            break
        except:
            pass

    # Take steps until we end up at the beginning again.  Keep track of path along the way.
    while cur_loc != s_loc:
        cur_loc, cur_direction = try_step_direction(map_matrix, cur_loc, cur_direction)
        travel_path.append(cur_loc)
    
    print('k')
    print(s_loc)
    print(travel_path)
    print(len(travel_path) / 2)

