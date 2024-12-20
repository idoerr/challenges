import re

if __name__ == "__main__":
    file_name = 'adventofcode2024/day3puz1input.txt'

    mul_pairs = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            for match in re.finditer("mul\((\d+),(\d+)\)", line):
                first_num = int(match.group(1))
                second_num = int(match.group(2))
                mul_pairs.append((first_num, second_num))

    print(mul_pairs)
    print(sum(map(lambda a: a[0]*a[1], mul_pairs)))