from collections import defaultdict
import re

if __name__ == "__main__":
    file_name = 'adventofcode2023/day3puz2input.txt'

    symbol_list = { '*', '+', '=', '-', '%', '$', '@', '#', '/', '=' }
    data_matrix = []

    def star_locations( target_row, start_col, end_col ):
        ret_list = []
        for row in range(target_row-1, target_row+2):
            if row < 0 or row >= len(data_matrix):
                continue;
            cur_row = data_matrix[row]
            for col in range(start_col-1, end_col+1):
                if col < 0 or col >= len(cur_row):
                    continue;
                cur_val = cur_row[col]
                if cur_val == '*':
                    ret_list.append((row, col))
        return ret_list
    
    star_collection = defaultdict(list)

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(line)
    
    for row, line in enumerate(data_matrix):
        for match in re.finditer('\d+', line):
            number = int(match.group(0))
            start_col = match.start()
            end_col = match.end()

            adjacent_stars = star_locations(row, start_col, end_col)

            for star_loc in adjacent_stars:
                star_collection[star_loc].append(number)
    
    print('almost done!')

    print(star_collection)

    print(sum(number_list[0] * number_list[1] for star_loc, number_list in star_collection.items() if len(number_list) == 2))