import numpy
from collections import defaultdict

def advance_second(position_matrix, velocity_matrix, width, height):
    new_positions = numpy.add(position_matrix, velocity_matrix)
    
    # values in the negative should have matrix bounds added to them.
    negative_mask = new_positions < 0
    add_array = numpy.repeat([(width, height)], len(position_matrix), axis=0)
    add_array = numpy.where(negative_mask, add_array, 0)
    # add_array = numpy.ma.masked_where(negative_mask, add_array)
    
    new_positions = numpy.add(new_positions, add_array)
    # new_positions = new_positions.compressed()

    # values above the max position should be modulo'd to be within range.
    new_positions = numpy.mod(new_positions, (width, height))
    return new_positions

def quadrant_score(position_matrix, width, height):
    top_left_score = 0
    top_right_score = 0
    bottom_left_score = 0
    bottom_right_score = 0

    exclude_arr = []

    for x, y in position_matrix:
        if y < height // 2:
            if x < width // 2:
                top_left_score += 1
            elif x > width // 2:
                top_right_score += 1
            else:
                exclude_arr.append((int(x), int(y)))
        elif y > height // 2:
            if x < width // 2:
                bottom_left_score += 1
            elif x > width // 2:
                bottom_right_score += 1
            else:
                exclude_arr.append((int(x), int(y)))
        else:
            exclude_arr.append((int(x), int(y)))
    print(top_left_score, top_right_score, bottom_left_score, bottom_right_score)
    return top_left_score * top_right_score * bottom_left_score * bottom_right_score


def print_matrix(position_matrix, width, height):

    position_counts = defaultdict(int)

    for pos in position_matrix:
        position_counts[str(pos)] += 1
    
    for y in range(height):
        row_str = ''
        for x in range(width):
            str_lookup = str(numpy.array([x, y]))
            if str_lookup in position_counts:
                row_str += str(position_counts[str_lookup])
            elif x == width // 2 or y == height // 2:
                row_str += '0'
            else:
                row_str += '.'
        print(row_str)

def check_for_unique(position_matrix):
    unique_positions = numpy.unique(position_matrix, axis=0)

    return len(position_matrix) == len(unique_positions)


if __name__ == '__main__':
    file_name = 'adventofcode2024/day14input.txt'

    position_matrix = []
    velocity_matrix = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            pos_str, vel_str = line.strip().split()
            pos_list = list(map(int, pos_str[2:].split(',')))
            vel_list = list(map(int, vel_str[2:].split(',')))

            position_matrix.append(pos_list)
            velocity_matrix.append(vel_list)
    
    position_matrix = numpy.array(position_matrix)

    width = 101
    height = 103
    second_count = 100

    # Part 1
    new_pos_matrix = position_matrix
    for i in range(second_count):
        new_pos_matrix = advance_second(new_pos_matrix, velocity_matrix, width, height)

    print(quadrant_score(new_pos_matrix, width, height))
    print()

    # Part 2 - The theory is that there christmas tree appearance is the initial setup of the puzzle
    # In this setup, there are no overlapping values.
    # This means that we will iterate until there are no overlapping values.
    # This means that len(unique rows in matrix) == len(rows in matrix)
    iter_count = 0
    while not check_for_unique(position_matrix):
        position_matrix = advance_second(position_matrix, velocity_matrix, width, height)
        iter_count += 1

    print_matrix(position_matrix, width, height)
    print()
    print(iter_count)
    print(quadrant_score(position_matrix, width, height))

    

