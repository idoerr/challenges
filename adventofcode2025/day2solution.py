import math

def is_invalid_id(num):
    num_digits = math.floor(math.log10(num)) + 1
    if num_digits % 2 == 1:
        return False

    mid_point_div = 10 ** (num_digits // 2)
    
    bottom_half = num % mid_point_div
    top_half = num // mid_point_div

    return bottom_half == top_half

def is_invalid_id_due_to_copies(num):
    num_digits = math.floor(math.log10(num)) + 1

    for divisor in range(2, num_digits + 1):
        # print(num, divisor, is_invalid_id_by_num_copies(num, divisor))
        if is_invalid_id_by_num_copies(num, divisor):
            return True

    return False

def is_invalid_id_by_num_copies(num, divisor):
    
    num_digits = math.floor(math.log10(num)) + 1

    if num_digits % divisor != 0:
        return False

    div_num = 10 ** (num_digits // divisor)

    check_num = num % div_num
    num_remain = num // div_num

    while num_remain > 0:
        num_modulo = num_remain % div_num
        if num_modulo != check_num:
            return False
        
        num_remain = num_remain // div_num
    
    return True

if __name__ == '__main__':
    file_name = 'adventofcode2025/day2input.txt'

    ranges = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            for range_str in line.split(','):
                start_range, end_range = range_str.split('-')
                ranges.append((int(start_range), int(end_range)))

    invalid_id_list = []
    invalid_id_list_part2 = []

    for start_range, end_range in ranges:
        for i in range(start_range, end_range + 1):
            if is_invalid_id(i):
                invalid_id_list.append(i)
            if is_invalid_id_due_to_copies(i):
                invalid_id_list_part2.append(i)
    
    print(sum(invalid_id_list))
    print(sum(invalid_id_list_part2))
