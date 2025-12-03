
def find_largest_in_range(row_vals):
    max_val_with_index = max(enumerate(row_vals), key=lambda x: (x[1], -x[0]))

    return max_val_with_index

def find_top_x_vals_in_order(row_vals, val_count):
    found_vals = []
    sub_row = row_vals

    for ignore_count in range(val_count - 1, -1, -1):
        search_row = sub_row[0:-ignore_count] if ignore_count > 0 else sub_row
        max_index, max_val = find_largest_in_range(search_row)

        found_vals.append(max_val)
        sub_row = sub_row[max_index + 1:]
    
    return found_vals

def digits_to_num(vals):
    result_num = 0
    for x in vals:
        result_num *= 10
        result_num += x
    
    return result_num


if __name__ == '__main__':
    file_name = 'adventofcode2025/day3input.txt'

    result_joltages_part1 = []
    result_joltages_part2 = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            row_joltages = list(int(x) for x in line.strip())

            top_joltages_part1 = find_top_x_vals_in_order(row_joltages, 2)
            end_joltage_part1 = digits_to_num(top_joltages_part1)
            result_joltages_part1.append(end_joltage_part1)

            top_joltages_part2 = find_top_x_vals_in_order(row_joltages, 12)
            end_joltage_part2 = digits_to_num(top_joltages_part2)
            result_joltages_part2.append(end_joltage_part2)


    print(sum(result_joltages_part1))
    print(sum(result_joltages_part2))
    