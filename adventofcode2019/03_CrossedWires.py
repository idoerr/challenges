
def get_points( wire_arr ):

    cur_x = 0
    cur_y = 0

    points_arr = []

    for wire_dir in wire_arr:
        dir_char = wire_dir[0]
        wire_len = int(wire_dir[1:])

        for step in range(1, wire_len + 1):
            if dir_char == 'U':
                new_loc = (cur_x, cur_y + step)
            elif dir_char == 'D':
                new_loc = (cur_x, cur_y - step)
            elif dir_char == 'R':
                new_loc = (cur_x + step, cur_y)
            elif dir_char == 'L':
                new_loc = (cur_x - step, cur_y)
            
            points_arr.append(new_loc)
        
        if dir_char == 'U':
            cur_y += wire_len
        elif dir_char == 'D':
            cur_y -= wire_len
        elif dir_char == 'R':
            cur_x += wire_len
        elif dir_char == 'L':
            cur_x -= wire_len
    
    return points_arr

def get_lines( wire_arr ):

    cur_x = 0
    cur_y = 0

    line_arr = []

    for wire_dir in wire_arr:
        dir_char = wire_dir[0]
        wire_len = int(wire_dir[1:])

        if dir_char == 'U':
            first_coord = (cur_x, cur_y)
            second_coord = (cur_x, cur_y + wire_len)
            cur_y += wire_len
        elif dir_char == 'D':
            first_coord = (cur_x, cur_y - wire_len)
            second_coord = (cur_x, cur_y)
            cur_y -= wire_len
        elif dir_char == 'R':
            first_coord = (cur_x, cur_y)
            second_coord = (cur_x + wire_len, cur_y)
            cur_x += wire_len
        elif dir_char == 'L':
            first_coord = (cur_x - wire_len, cur_y)
            second_coord = (cur_x, cur_y)
            cur_x -= wire_len
        
        line_arr.append( (first_coord, second_coord) )
    
    return line_arr

def line_intersection(first_line, second_line):

    is_first_vert = first_line[0][0] == first_line[1][0]
    is_second_vert = second_line[0][0] == second_line[1][0]

    if is_first_vert == is_second_vert:
        return None
    
    if not is_first_vert:
        temp = first_line
        first_line = second_line
        second_line = temp
    
    f_l_coord = first_line[0]
    f_r_coord = first_line[1]

    f_l_x = f_l_coord[0]
    f_r_x = f_r_coord[0]
    f_l_y = f_l_coord[1]
    f_r_y = f_r_coord[1]

    s_l_coord = second_line[0]
    s_r_coord = second_line[1]

    s_l_x = s_l_coord[0]
    s_r_x = s_r_coord[0]
    s_l_y = s_l_coord[1]
    s_r_y = s_r_coord[1]
    
    if s_l_x > f_l_x or s_r_x < f_l_x:
        return None
    
    if f_l_y > s_l_y or f_r_y < s_l_y:
        return None
    
    return (f_l_x, s_l_y)
    

def manhattan_distance(first_tuple, second_tuple):
    return sum(abs(a - b) for a,b in zip(first_tuple, second_tuple))

def manhattan_origin(tup):
    return sum(abs(x) for x in tup)

input_file = 'adventofcode2019/03_CrossedWires.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    first_wire_str = file_obj.readline()
    first_wire_arr = first_wire_str.split(',')

    first_wires = get_lines(first_wire_arr)
    first_points = get_points(first_wire_arr)

    second_wire_str = file_obj.readline()
    second_wire_arr = second_wire_str.split(',')

    second_wires = get_lines(second_wire_arr)
    second_points = get_points(second_wire_arr)

    intersections = set(first_points) & set(second_points)

    # for f_wire in first_wires:
    #     for s_wire in second_wires:
    #         intersect = line_intersection(f_wire, s_wire)
    #         if intersect is not None and intersect != (0,0):
    #             intersections.append(intersect)
    
    # Part 1 result
    print("Part 1 result")
    result = min(intersections, key=manhattan_origin)
    print(result)
    print(manhattan_origin(result))

    print()
    print("Part 2 result")

    def wire_step_distance(point):
        first_steps = 1 + first_points.index(point)
        second_steps = 1 + second_points.index(point)
        return first_steps + second_steps
    
    result = min(intersections, key=wire_step_distance)
    print(result)
    print(wire_step_distance(result))

    