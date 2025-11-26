import math
import itertools
import re

def preprocess_grid_to_directions(button_grid, blank_point):
    lookup_map = {}
    # Iterate through each [row, col] combination in the grid.
    # Iterate through every permutation of pair points in the gride
    for i_row_1, row_1 in enumerate(button_grid):
        for i_col_1, char_1 in enumerate(row_1):

            for i_row_2, row_2 in enumerate(button_grid):
                for i_col_2, char_2 in enumerate(row_2):

                    start_point = (i_row_1, i_col_1)
                    end_point = (i_row_2, i_col_2)

                    direction_permutes = generate_direction_commands(start_point, end_point, blank_point)

                    lookup_map[(char_1, char_2)] = direction_permutes
    return lookup_map

# Iterate through each step of directions, return False if we land on the blank point
def is_valid_direction_set(directions, start_point, blank_point):
    cur_point = start_point
    for x in directions:
        if x == '^':
            cur_point = cur_point[0] - 1, cur_point[1]
        elif x == 'v':
            cur_point = cur_point[0] + 1, cur_point[1]
        elif x == '<':
            cur_point = cur_point[0], cur_point[1] - 1
        elif x == '>':
            cur_point = cur_point[0], cur_point[1] + 1
        
        if cur_point == blank_point:
            return False
    return True

def generate_single_dir_command(start_point, end_point):
    row_distance = end_point[0] - start_point[0]
    col_distance = end_point[1] - start_point[1]

    if col_distance > 0:
        horizontal_dirs = '>' * abs(col_distance)
    else:
        horizontal_dirs = '<' * abs(col_distance)

    if row_distance < 0:
        vertical_dirs = '^' * abs(row_distance)
    else:
        vertical_dirs = 'v' * abs(row_distance)

    return horizontal_dirs + vertical_dirs

# Direction commands between points consist of '<>' and '^v' chars
# We know that repeating a direction command will always be faster than constantly
# changing directions.  IE >>^^ is always better then >^>^
# This means the only question is whether to move horizontally or vertically first.
def generate_direction_commands(start_point, end_point, blank_point):
    row_distance = end_point[0] - start_point[0]
    col_distance = end_point[1] - start_point[1]

    if col_distance > 0:
        horizontal_dirs = '>' * abs(col_distance)
    else:
        horizontal_dirs = '<' * abs(col_distance)

    if row_distance < 0:
        vertical_dirs = '^' * abs(row_distance)
    else:
        vertical_dirs = 'v' * abs(row_distance)

    possible_combos = [horizontal_dirs + vertical_dirs + 'A', vertical_dirs + horizontal_dirs + 'A']
    # filter out combinations where we hit the blank point
    return list(filter(lambda x: is_valid_direction_set(x, start_point, blank_point), possible_combos ))

number_keypad_buttons = (('7', '8', '9'), ('4', '5', '6'), ('1', '2', '3'), (' ', '0', 'A'))
directional_keypad_buttons = ((' ', '^', 'A'), ('<', 'v', '>'))

number_keypad_directions = preprocess_grid_to_directions(number_keypad_buttons, (3, 0))
directional_keypad_directions = preprocess_grid_to_directions(directional_keypad_buttons, (0, 0))

def calc_code_entry_path_recurse(code, robot_count_remaining, max_robots=-1, code_sequences_memo={}):
    # Initialization case.  Note that the memo is also initialized in this case
    if max_robots == -1:
        max_robots = robot_count_remaining
    
    # Memo-ize lookup
    if (code, robot_count_remaining) in code_sequences_memo:
        return code_sequences_memo[(code, robot_count_remaining)]
    
    # Base case
    if robot_count_remaining == 0:
        return len(code)
    
    # If this is the first level
    if robot_count_remaining == max_robots:
        keypad_direction_map = number_keypad_directions
    else:
        keypad_direction_map = directional_keypad_directions
    
    number_key_presses = 0

    # Calculate the transitions using pairs of letters.
    # We know that every code ends in A.  This means that we will always start with the robot on 'A'
    # So the first step will always be between 'A' and 'first code letter'
    # Since we know the start point, we can prepend that to the string, to replace indexing
    for key_pairs in zip('A' + code, code):
        possible_combos = keypad_direction_map[key_pairs]

        # Our recursion case, note keeping max_robots and code_sequences_memo
        def recurse_func(combo):
            return calc_code_entry_path_recurse(combo, robot_count_remaining - 1, max_robots, code_sequences_memo)

        # Recurse each possible combo, but only keep the minimum length
        min_code_length = min( map(recurse_func, possible_combos ) )

        number_key_presses += min_code_length
    
    code_sequences_memo[(code, robot_count_remaining)] = number_key_presses

    return number_key_presses

def calc_command_score(command, button_presses):
    # return int(command[0:-1]) * len(button_presses)
    return int(command[0:-1]) * button_presses

if __name__ == '__main__':
    file_name = 'adventofcode2024/day21input.txt'

    command_list = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            command_list.append(line.strip())

    # command_list = ['029A']

    # part 1
    total_score_part1 = 0
    for command in command_list:
        button_press_count = calc_code_entry_path_recurse(command, 3)
        total_score_part1 += calc_command_score(command, button_press_count)
        print(command, button_press_count, calc_command_score(command, button_press_count))
    
    print(total_score_part1)

    # part 2
    total_score_part2 = 0
    for command in command_list:
        button_press_count = calc_code_entry_path_recurse(command, 26)
        total_score_part2 += calc_command_score(command, button_press_count)
        print(command, button_press_count, calc_command_score(command, button_press_count))
    
    print(total_score_part2)

