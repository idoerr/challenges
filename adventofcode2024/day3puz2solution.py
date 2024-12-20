import re

if __name__ == "__main__":
    file_name = 'adventofcode2024/day3puz1input.txt'

    mul_pairs = []
    is_enabled = True

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            for match in re.finditer("(?:(mul)\((\d+),(\d+)\))|(?:(do)\(\))|(?:(don't)\(\))", line):
                match_type = match.group(1) or match.group(4) or match.group(5)

                if match_type == 'do':
                    is_enabled = True
                elif match_type == "don't":
                    is_enabled = False
                elif is_enabled and match_type == 'mul':
                    first_num = int(match.group(2))
                    second_num = int(match.group(3))
                    mul_pairs.append((first_num, second_num))

    print(mul_pairs)
    print(sum(map(lambda a: a[0]*a[1], mul_pairs)))