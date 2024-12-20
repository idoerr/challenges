import time
import itertools
import math

def recurse_operator_insert_part1(target, num_list):

    if len(num_list) == 1:
        yield num_list[0]
    else:
        for x in recurse_operator_insert_part1(target, num_list[0:-1]):
            mod_num = num_list[-1] + x
            if mod_num <= target:
                yield(mod_num)

            mod_num = num_list[-1] * x
            if mod_num <= target:
                yield(mod_num)

def recurse_operator_insert_part2(target, num_list):

    if len(num_list) == 1:
        yield num_list[0]
    else:
        for x in recurse_operator_insert_part2(target, num_list[0:-1]):
            mod_num = num_list[-1] + x
            if mod_num <= target:
                yield(mod_num)

            mod_num = num_list[-1] * x
            if mod_num <= target:
                yield(mod_num)

            mod_num = x * (10 ** math.floor(math.log(num_list[-1], 10) + 1)) + num_list[-1]
            if mod_num <= target:
                yield(mod_num)

calibration_gen = {}

def gen_calibration_options(num_list):

    operator_count = len(num_list) - 1
    if operator_count in calibration_gen:
        operator_possibilities = calibration_gen[operator_count]
    else:
        operator_possibilities = list(itertools.product([0, 1], repeat=len(num_list)-1))
        calibration_gen[operator_count] = operator_possibilities

    for operator_list in operator_possibilities:
        gen_num = num_list[0]
        for operator in operator_list:
        # for num, operator in zip(num_list[1:], operator_list):
            # if operator == 0:
            #     gen_num += num
            # elif operator == 1:
            #     gen_num *= num
            yield gen_num


if __name__ == "__main__":
    file_name = 'adventofcode2024/day7input.txt'

    start_time = time.time()

    valid_calibrations_p1 = []
    valid_calibrations_p2 = []

    max_list = 0

    row = 0
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            left, right = line.split(': ', 2)
            calibration_num = int(left)

            num_list = list(map(int, right.split(' ')))
            max_list = max(max_list, len(num_list))

            print(calibration_num, len(num_list))

            #for x in gen_calibration_options(num_list):
            for x in recurse_operator_insert_part1(calibration_num, num_list):
                if x == calibration_num:
                    valid_calibrations_p1.append(x)
                    break

            for x in recurse_operator_insert_part2(calibration_num, num_list):
                if x == calibration_num:
                    valid_calibrations_p2.append(x)
                    break
    
    print()
    print(max_list)
    print(sum(valid_calibrations_p1))
    print(sum(valid_calibrations_p2))
    print("--- %s seconds ---" % (time.time() - start_time))
