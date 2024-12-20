from collections import defaultdict

if __name__ == "__main__":
    file_name = 'adventofcode2024/day1puz1input.txt'

    left_list = []
    right_dict = defaultdict(int)

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            left_str, right_str = line.split(' ', 1)

            left_list.append(int(left_str))

            right_dict[int(right_str)] += 1

    left_list = sorted(left_list)

    delta_list = []
    for left in left_list:
        delta_list.append(abs(left * right_dict[left]))
    
    print(sum(delta_list))
