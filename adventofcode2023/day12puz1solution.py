
import datetime

def is_valid_combination(spring_layout, broken_spring_counts):
    broken_index = 0

    broken_concat_count = 0

    for x in spring_layout:
        if x == '#':
            broken_concat_count += 1
        else:
            if broken_concat_count > 0:
                if broken_index >= len(broken_spring_counts):
                    return False
                if broken_spring_counts[broken_index] != broken_concat_count:
                    return False
                broken_index += 1
            broken_concat_count = 0
    
    if broken_concat_count > 0:
        if broken_index >= len(broken_spring_counts):
            return False
        if broken_spring_counts[broken_index] != broken_concat_count:
            return False
        broken_index += 1
    
    return broken_index == len(broken_spring_counts)

def generate_valid_combinations(match_str, broken_spring_counts):
    str_len = len(match_str)
    broken_spring_strs = []
    for x in broken_spring_counts:
        broken_spring_strs.append('#' * x + '.')
    broken_spring_strs[-1] = broken_spring_strs[-1][0:-1]

    max_dots = str_len - sum(broken_spring_counts) - len(broken_spring_counts) + 1

    ret_arr = []
    generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, '', 0, 0, ret_arr)
    return ret_arr

def generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, partial_build, spring_index, dot_count, ret_arr):
    if not question_str_equals(match_str, partial_build):
        return
    if spring_index == len(broken_spring_strs) and dot_count == max_dots:
        ret_arr.append(partial_build)
    elif spring_index == len(broken_spring_strs):
        partial_build = partial_build + '.'
        generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, partial_build, spring_index, dot_count + 1, ret_arr)
    elif dot_count == max_dots:
        partial_build = partial_build + broken_spring_strs[spring_index]
        generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, partial_build, spring_index + 1, dot_count, ret_arr)
    else:
        partial_build_dot = partial_build + '.'
        generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, partial_build_dot, spring_index, dot_count + 1, ret_arr)

        partial_build_spring = partial_build + broken_spring_strs[spring_index]
        generate_valid_combinations_recurse(match_str, broken_spring_strs, max_dots, partial_build_spring, spring_index + 1, dot_count, ret_arr)

def question_str_equals(question_str, build_str):
    for a, b in zip(question_str, build_str):
        if a != '?' and a != b:
            return False
    return True

if __name__ == "__main__":
    file_name = 'adventofcode2023/day12puz1input.txt'

    start = datetime.datetime.now()

    row_valid_combinations = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            spring_layout, indexes = line.split(' ', 1)
            print(spring_layout, indexes)

            broken_spring_counts = list(map(int, indexes.split(',')))
            max_pound = sum(broken_spring_counts)
            max_dot = len(spring_layout) - max_pound

            valid_layouts = generate_valid_combinations(spring_layout, broken_spring_counts)
            valid_combinations = len(valid_layouts)
            
            #print(2 ** spring_layout.count('?'), len(check_layouts), len(valid_layout))
            row_valid_combinations.append(valid_combinations)

    print(sum(row_valid_combinations))

    end = datetime.datetime.now()

    print(end - start)

