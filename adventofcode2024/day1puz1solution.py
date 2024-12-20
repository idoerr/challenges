

if __name__ == "__main__":
    file_name = 'adventofcode2024/day1puz1input.txt'

    left_list = []
    right_list = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            left_str, right_str = line.split(' ', 1)

            left_list.append(int(left_str))
            right_list.append(int(right_str))

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    delta_list = []
    for left, right in zip(left_list, right_list):
        delta_list.append(abs(left - right))
    
    print(sum(delta_list))
