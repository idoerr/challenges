
def add_points(a, b):
    return a[0] + b[0], a[1] + b[1]

def handle_robot_move(warehouse_map, robot_location, move):

    if move == '<':
        location_offset = (0, -1)
    elif move == '>':
        location_offset = (0, 1)
    elif move == '^':
        location_offset = (-1, 0)
    elif move == 'v':
        location_offset = (1, 0)
    else:
        return robot_location

    move_set = set()
    move_queue = [robot_location]
    check_location = add_points(robot_location, location_offset)
    check_queue = [check_location]

    while len(check_queue) > 0:
        object_location = check_queue.pop()
        object_contents = warehouse_map[object_location[0]][object_location[1]]

        if object_contents == '#':
            return robot_location
        elif object_contents in ('O', '[', ']'):
            if str(object_location) not in move_set:
                move_set.add(str(object_location))
                move_queue.append(object_location)
            check_location = add_points(object_location, location_offset)
            check_queue.append(check_location)

            if move in ('^', 'v' ) and object_contents != 'O':
                second_location_offset = (0, 1) if object_contents == '[' else (0, -1)
                second_location = add_points(object_location, second_location_offset)
                if str(second_location) not in move_set:
                    move_set.add(str(second_location))
                    move_queue.append(second_location)
                
                second_check_offset = (-1, 0) if move == '^' else (1, 0)
                second_check_location = add_points(second_location, second_check_offset)
                check_queue.append(second_check_location)
        else:
            # move_queue.append(object_location)
            continue

    # When moving we need to process rows in order
    # Otherwise, we may end up overwriting cells we don't mean to.
    if move == '^':
        move_queue = sorted(move_queue, reverse=True)
    elif move == 'v':
        move_queue = sorted(move_queue)

    for orig_loc in reversed(move_queue):
        move_loc = add_points(orig_loc, location_offset)

        orig_contents = warehouse_map[orig_loc[0]][orig_loc[1]]
        warehouse_map[orig_loc[0]][orig_loc[1]] = '.'
        warehouse_map[move_loc[0]][move_loc[1]] = orig_contents
    
    return add_points(robot_location, location_offset)

def calculate_gps_sum(warehouse_map):
    gps_sum = 0
    for i_row, row in enumerate(warehouse_map):
        for i_col, col in enumerate(row):
            if col in ('O', '['):
                gps_sum += 100 * i_row + i_col
    return gps_sum

def print_warehouse_map(warehouse_map):
    for x in warehouse_map:
        print(''.join(x))

if __name__ == '__main__':
    file_name = 'adventofcode2024/day15input.txt'

    warehouse_map = []
    movement_list = ''

    found_blank_line = False

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            line = line.strip()
            if line == '':
                found_blank_line = True
            elif found_blank_line:
                movement_list += line
            else:
                warehouse_map.append([x for x in line])

    # First determine the starting location of the robot
    start_robot_location = None
    for i_row, row in enumerate(warehouse_map):
        for i_col, col in enumerate(row):
            if col == '@':
                start_robot_location = (i_row, i_col)

    # print_warehouse_map(warehouse_map)
    # print()
    
    # Part 1
    robot_location = start_robot_location
    map_copy = list(list(x) for x in warehouse_map)
    for move in movement_list:
        robot_location = handle_robot_move(map_copy, robot_location, move)

    print_warehouse_map(map_copy)
    print()
    print(calculate_gps_sum(map_copy))
    print()

    # Part 2
    robot_location = (start_robot_location[0], start_robot_location[1] * 2)

    def fatten_row(row):
        for x in row:
            if x == 'O':
                yield '['
                yield ']'
            elif x == '@':
                yield '@'
                yield '.'
            else:
                yield x
                yield x

    fat_map_copy = list(map(lambda row: list(fatten_row(row)), warehouse_map))

    print_warehouse_map(fat_map_copy)
    print()

    for i, move in enumerate(movement_list):
        robot_location = handle_robot_move(fat_map_copy, robot_location, move)

    print_warehouse_map(fat_map_copy)
    print()
    print(calculate_gps_sum(fat_map_copy))
    

    
