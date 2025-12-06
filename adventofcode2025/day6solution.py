from collections import defaultdict
from functools import reduce

def calc_column_problems(column_vals, column_operators):
    column_results = []

    for i, operator in enumerate(column_operators):
        if operator == '*':
            column_value = reduce(lambda out, val: out * int(val), column_vals[i], 1)
        else:
            column_value = reduce(lambda out, val: out + int(val), column_vals[i], 0)
        column_results.append(column_value)
    
    return column_results

if __name__ == '__main__':
    file_name = 'adventofcode2025/day6input.txt'

    row_strs = []

    column_vals = defaultdict(list)
    column_operators = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            if line.find('*') == -1:
                row_strs.append(line[:-1])
                for i, val in enumerate(line.strip().split()):
                    column_vals[i].append(val)
            else:
                column_operators = line.strip().split()
    
    cur_problem = 0
    column_rotate_vals = defaultdict(list)

    max_len = len(max(row_strs, key=len))

    for i in range(max_len):
        col_val = ''

        for row in row_strs:
            if i >= len(row):
                col_val += ' '
            else:
                col_val += row[i]
        
        if col_val.strip() == '':
            cur_problem += 1
        else:
            column_rotate_vals[cur_problem].append(col_val)

    
    column_results_part1 = calc_column_problems(column_vals, column_operators)
    print(sum(column_results_part1))

    column_results_part2 = calc_column_problems(column_rotate_vals, column_operators)
    print(sum(column_results_part2))

    # print(sum(column_results))

    