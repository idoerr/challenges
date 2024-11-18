import re

if __name__ == "__main__":
    file_name = 'adventofcode2023/day3puz1input.txt'

    symbol_list = { '*', '+', '=', '-', '%', '$', '@', '#', '/', '=' }
    data_matrix = []

    def valid_number( target_row, start_col, end_col ):
        for row in range(target_row-1, target_row+2):
            if row < 0 or row >= len(data_matrix):
                continue;
            cur_row = data_matrix[row]
            for col in range(start_col-1, end_col+1):
                if col < 0 or col >= len(cur_row):
                    continue;
                cur_val = cur_row[col]
                if (not cur_val.isnumeric()) and cur_val != '.' and cur_val != '\n':
                    return True
        return False
    
    number_list = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(line)
    
    for row, line in enumerate(data_matrix):
        for match in re.finditer('\d+', line):
            number = int(match.group(0))
            start_col = match.start()
            end_col = match.end()

            if valid_number(row, start_col, end_col):
                number_list.append(number)
    
    print('almost done!')

    print(sum(number_list))