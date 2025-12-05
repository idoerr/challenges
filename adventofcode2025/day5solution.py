
from functools import reduce

def is_ingredient_fresh( ingredient_id, fresh_ranges):
    
    for start_range, end_range in fresh_ranges:
        if ingredient_id >= start_range and ingredient_id <= end_range:
            return True
    
    return False

def combine_overlapping_ranges(range_list):

    i = 0

    while i < len(range_list) - 1:
        start_range_1, end_range_1 = range_list[i]
        start_range_2, end_range_2 = range_list[i+1]

        if end_range_1 >= start_range_2:
            # Do combine elements

            new_start_range = min(start_range_1, start_range_2)
            new_end_range = max(end_range_1, end_range_2)

            range_list[i] = (new_start_range, new_end_range)

            del range_list[i+1]
            
        else:
            i += 1

if __name__ == '__main__':
    file_name = 'adventofcode2025/day5input.txt'

    fresh_ranges = []
    ingredient_ids = []

    reading_fresh_ranges = True
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            if line.strip() == '':
                reading_fresh_ranges = False
            elif reading_fresh_ranges:
                start_range, end_range = line.strip().split('-')
                fresh_ranges.append((int(start_range), int(end_range)))
            else:
                ingredient_ids.append(int(line))

    fresh_ranges = sorted(fresh_ranges)
    combine_overlapping_ranges(fresh_ranges)

    fresh_count = reduce(lambda out, item: out + (1 if is_ingredient_fresh(item, fresh_ranges) else 0), ingredient_ids, 0)
    print(fresh_count)

    fresh_ingredient_count = reduce(lambda count, check_range: count + check_range[1] - check_range[0] + 1, fresh_ranges, 0)
    print(fresh_ingredient_count)
    