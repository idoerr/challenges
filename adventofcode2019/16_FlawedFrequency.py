
import datetime
import math
import numpy as np
import cProfile

input_file = 'adventofcode2019/16_FlawedFrequency.txt'

def calc_pattern_for_index(base_pattern, index, max_len):
    # in-place element repeat based on our index count
    cur_pattern = np.repeat(base_pattern, index)

    # tile the list until it is at least as long as the input string.
    tile_count = math.ceil((max_len + 1.0 / len(cur_pattern)))
    cur_pattern = np.tile(cur_pattern, tile_count)

    # Remove the first element of the pattern.
    cur_pattern = cur_pattern[1:]

    # Cut off any extra values
    cur_pattern = cur_pattern[0:max_len]
    return cur_pattern

def calc_new_index_value(value_list, pattern_list, index):
    return abs(np.sum(np.multiply(value_list, pattern_list[index]))) % 10

def apply_phase(value_list, pattern_list):
    return [calc_new_index_value(value_list, pattern_list, i) for i in range(len(value_list))]

def apply_phase_matrix(value_list, pattern_list):
    # return np.abs(np.dot(pattern_list, value_list))
    return np.mod(np.abs(np.dot(pattern_list, value_list)), 10)

if __name__ == "__main__":

    start = datetime.datetime.now()

    file_obj = open(input_file, 'r')
    char_str = file_obj.readline().strip()

    value_list = list(map(int, char_str))

    pattern = [0,1,0,-1]
    pattern_matrix = [calc_pattern_for_index(pattern, i+1, len(value_list)) for i in range(len(value_list))]

    print(datetime.datetime.now() - start)

    new_list = value_list

    for i in range(100):
        print(new_list)
        new_list = apply_phase_matrix(new_list, pattern_matrix)

    print(datetime.datetime.now() - start)
    print("Part 1 Result")
    print(new_list[0:8])

    start = datetime.datetime.now()
    
    part2_list = np.tile(value_list, 100)
    pattern_matrix = np.empty((len(part2_list), len(part2_list)))

    # cProfile.run("[calc_pattern_for_index(pattern, i+1, len(part2_list)) for i in range(len(part2_list))]")
    
    for i in range(len(part2_list)):
        pattern_matrix[i,:] = calc_pattern_for_index(pattern, i+1, len(part2_list))
    # pattern_matrix = [calc_pattern_for_index(pattern, i+1, len(part2_list)) for i in range(len(part2_list))]

    print(datetime.datetime.now() - start)

    new_list = part2_list
    for i in range(1):
        new_list = apply_phase_matrix(new_list, pattern_matrix)
    
    print(datetime.datetime.now() - start)

    print("Part 2 Result")
    print(new_list[0:8])


    

        