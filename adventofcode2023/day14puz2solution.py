
from collections import defaultdict
import bisect

def transpose(matrix):
    ret_matrix = []

    for _ in range(len(matrix[0])):
        ret_matrix.append([])
    
    for row in matrix:
        for col_num, cell in enumerate(row):
            ret_matrix[col_num].append(cell)
    
    return tuple(tuple(x) for x in ret_matrix)

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

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        if self._is_transposed == other._is_transposed:
            return self._matrix == other._matrix
        else:
            return self._matrix == other._col_matrix

    def __hash__(self):
        if self._is_transposed:
            return hash(self._col_matrix)
        else:
            return hash(self._matrix)
        
    def __str__(self):
        ret_str = ''
        for row in self.get_rows_gen():
            for col in row:
                ret_str += col
            ret_str += '\n'
        return ret_str

#The tilt methods
def do_four_direction_tilt(matrix_obj:Matrix):
    ret_matrix = tilt_toward_north(matrix_obj)
    ret_matrix = tilt_toward_west(ret_matrix)
    ret_matrix = tilt_toward_south(ret_matrix)
    ret_matrix = tilt_toward_east(ret_matrix)

    return ret_matrix

def tilt_toward_north( matrix_obj:Matrix ):

    new_matrix = []
    for col in matrix_obj.get_cols_gen():
        tilt_col = tilt_toward_beginning(col)
        new_matrix.append(tilt_col)

    ret_matrix = Matrix(False, new_matrix)
    ret_matrix.transpose()

    return ret_matrix

def tilt_toward_south( matrix_obj:Matrix ):
    new_matrix = []
    for col in matrix_obj.get_cols_gen():
        tilt_col = tilt_toward_beginning(reversed(col))
        new_matrix.append(tuple(reversed(tilt_col)))
    
    ret_matrix = Matrix(False, new_matrix)
    ret_matrix.transpose()

    return ret_matrix

def tilt_toward_west( matrix_obj:Matrix ):
    new_matrix = []
    for row in matrix_obj.get_rows_gen():
        tilt_row = tilt_toward_beginning(row)
        new_matrix.append(tilt_row)
    
    ret_matrix = Matrix(False, new_matrix)

    return ret_matrix

def tilt_toward_east( matrix_obj:Matrix ):
    new_matrix = []
    for row in matrix_obj.get_rows_gen():
        tilt_row = tilt_toward_beginning(reversed(row))
        new_matrix.append(tuple(reversed(tilt_row)))
    
    ret_matrix = Matrix(False, tuple(new_matrix))

    return ret_matrix

# single row tilt method
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
    
    return tuple(output_str)

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
    file_name = 'adventofcode2023/day14puz2input.txt'

    with open(file_name, 'r') as file_handle:

        matrix = []

        for line in file_handle:
            matrix.append(tuple(line.strip()))

    matrix_obj = Matrix(False, tuple(matrix))
    tilt_matrix = matrix_obj

    # take steps until we find that we have been at this step before.
    matrix_next_map = {}
    for i in range(100000):
        
        new_matrix = do_four_direction_tilt(tilt_matrix)
        matrix_next_map[tilt_matrix] = new_matrix
        tilt_matrix = new_matrix

        if new_matrix in matrix_next_map:
            break
    
    steps_taken_so_far = len(matrix_next_map)

    cycle_len = 1
    next_matrix = matrix_next_map[tilt_matrix]
    while next_matrix != tilt_matrix:
        next_matrix = matrix_next_map[next_matrix]
        cycle_len += 1

    steps_remaining = 1000000000 - steps_taken_so_far
    step_cycle_remainder = steps_remaining % cycle_len

    final_matrix = tilt_matrix
    for i in range(step_cycle_remainder):
        final_matrix = matrix_next_map[final_matrix]

    print('k')
    print(steps_taken_so_far)
    print(cycle_len)

    print()
    print(matrix_rounds_cost(final_matrix))
