

if __name__ == "__main__":
    file_name = '2023/day1puz1input.txt'

    row_values = [];

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            digits = [];

            for c in line:
                if c.isnumeric():
                    digits.append(int(c));

            value = digits[0] * 10 + digits[-1]

            row_values.append(value)

    print(sum(row_values))




