from collections import defaultdict
import itertools

def blink_rocks_recurse(rock_val, blinks_remaining, memo_map):

    if blinks_remaining == 0:
        return 1

    if (rock_val, blinks_remaining) in memo_map.keys():
        return memo_map[(rock_val, blinks_remaining)]

    next_level_blinks = blinks_remaining - 1
    
    if rock_val == 0:
        new_rock_val = 1

        recurse_result = blink_rocks_recurse(new_rock_val, next_level_blinks, memo_map)
        memo_map[(rock_val, blinks_remaining)] = recurse_result
        return recurse_result
    
    str_rock_val = str(rock_val)
    len_rock_val = len(str_rock_val)

    if len_rock_val % 2 == 0:
        half_len = len_rock_val // 2
        left_rock_val = str_rock_val[0:half_len]
        right_rock_val = str_rock_val[half_len:len_rock_val]

        recurse_result = blink_rocks_recurse(int(left_rock_val), next_level_blinks, memo_map) \
            + blink_rocks_recurse(int(right_rock_val), next_level_blinks, memo_map)
        memo_map[(rock_val, blinks_remaining)] = recurse_result
        return recurse_result
    else:
        recurse_result = blink_rocks_recurse(rock_val * 2024, next_level_blinks, memo_map)
        memo_map[(rock_val, blinks_remaining)] = recurse_result
        return recurse_result


if __name__ == "__main__":
    file_name = 'adventofcode2024/day11input.txt'

    start_row = []

    row = 0
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            start_row.extend(map(int, line.strip().split()))

    final_rock_count = 0

    for start_num in start_row:
        final_rock_count += blink_rocks_recurse(start_num, 75, {})

    print(final_rock_count)
    
