
from collections import defaultdict
import bisect

def transpose(matrix):
    ret_matrix = []

    for _ in range(len(matrix[0])):
        ret_matrix.append([])
    
    for row in matrix:
        for col_num, cell in enumerate(row):
            ret_matrix[col_num].append(cell)
    
    return ret_matrix

class Matrix:

    def __init__(self, is_transposed: bool, matrix):
        self._is_transposed = is_transposed
        self._matrix = matrix
        self._col_matrix = transpose(matrix)
    
    def transpose(self):
        self._is_transposed = not self._is_transposed

    def get_matrix(self):
        if self._is_transposed:
            return self._col_matrix
        else:
            return self._matrix
    
    def get_rows_gen(self):
        if self._is_transposed:
            for col in self._col_matrix:
                yield col
        else:
            for row in self._matrix:
                yield row

    def get_cols_gen(self):
        if self._is_transposed:
            for row in self._matrix:
                yield row
        else:
            for col in self._col_matrix:
                yield col

def tilt_toward_north( matrix_obj:Matrix ):

    new_matrix = []
    for col in matrix_obj.get_cols_gen():
        tilt_col = tilt_toward_beginning(col)
        new_matrix.append(tilt_col)

    ret_matrix = Matrix(False, new_matrix)
    ret_matrix.transpose()

    return ret_matrix

def tilt_toward_beginning( row ):
    cube_locations = []
    round_locations = []

    row_len = 0

    #Extract the cube and round locations
    for i, x in enumerate(row):
        row_len = i+1
        if x == '#':
            cube_locations.append(i)
        elif x == 'O':
            round_locations.append(i)

    rounds_behind_cubes = defaultdict(int)
    # find the nearest cube location, and find how many rounds match that 
    for x in round_locations:
        cube_index = bisect.bisect(cube_locations, x) - 1
        rounds_behind_cubes[cube_index] += 1

    # re-create the new state of the row
    output_str = ''
    
    # Start by adding a bunch of rounds that occur before the first cube.
    start_cube_count = rounds_behind_cubes[-1]
    output_str += 'O' * start_cube_count

    for cube_index, cube_location in enumerate(cube_locations):

        # Add a bunch of blanks to make fill the cube.
        if len(output_str) < cube_location:
            output_str += '.' * (cube_location - len(output_str))

        # Add in the rocks 
        rounds_behind_count = rounds_behind_cubes[cube_index]
        output_str += '#' + 'O' * rounds_behind_count

    # Pad out the row so that it is the same length as the original.
    if len(output_str) < row_len:
        output_str += '.' * (row_len - len(output_str))
    
    return output_str

def matrix_rounds_cost(matrix_obj:Matrix):

    # calculate the column cost
    column_costs = []
    for col in matrix_obj.get_cols_gen():
        column_costs.append(rounds_cost(col))
    
    return sum(column_costs)

def rounds_cost(row):
    total_cost = 0
    for i, x in enumerate(row):
        if x == 'O':
            cost = len(row) - i
            total_cost += cost
    return total_cost

if __name__ == "__main__":
    file_name = 'adventofcode2023/day14puz1input.txt'

    with open(file_name, 'r') as file_handle:

        matrix = []

        for line in file_handle:
            matrix.append(line.strip())

    matrix_obj = Matrix(False, matrix)
    
    tilt_matrix = tilt_toward_north(matrix_obj)

    result_matrix = tilt_matrix.get_matrix()

    print('x')
    for row in result_matrix:
        print_str = ''
        for col in row:
            print_str += col
        print(print_str)

    print()
    print(matrix_rounds_cost(tilt_matrix))
