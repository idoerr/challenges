
def find_xmas( search_str ):

    if len(search_str) < 4:
        return 0

    # transpose returns a list, so convert back to string as necessary.
    if isinstance(search_str, list):
        search_str = ''.join(search_str)

    # remember to search backwards.
    rev_str = ''.join(reversed(search_str))

    find_count = 0
    
    for i in range(len(search_str) - 3):
        # Sub-strings in python are O(1), so this should be fine for performance.
        if search_str[i:i+4] == 'XMAS':
            find_count += 1
        if rev_str[i:i+4] == 'XMAS':
            find_count += 1
    
    return find_count

def transpose(matrix):
    ret_matrix = []

    for _ in range(len(matrix[0])):
        ret_matrix.append([])
    
    for row in matrix:
        for col_num, cell in enumerate(row):
            ret_matrix[col_num].append(cell)
    
    return ret_matrix

# We are going to iterate over the matrix, using a diagonal pattern.
# The iteration range will go outside the matrix range, in a diagonal pattern.
# As long as the diagonal will touch the matrix, then it is included.
# This results in a total of (rows + columns - 1) diagonals, all of various lengths
# In the following example, the actual matrix is enclosed by '|' and 
# each diagonal is denoted by a single letter.
# Note that there are two sets of diagonals.
# ABCD|EFGHIJK|
#  ABC|DEFGHIJ|K
#   AB|CDEFGHI|JK
#    A|BCDEFGH|IJK
#     |ABCDEFG|HIJK
def generate_diagonals(matrix):

    row_count = len(matrix)
    col_count = len(matrix[0])
    # south-east pointing diagonals
    for start_col in range(-row_count + 1, col_count):
        diag_contents = []
        for index in range(row_count):
            col = start_col + index
            row = index

            if col >= 0 and col < col_count:
                diag_contents.append(matrix[row][col])
        yield diag_contents
    
    for start_col in range(0, row_count + col_count - 1):
        diag_contents = []
        for index in range(row_count):
            col = start_col - index
            row = index

            if col >= 0 and col < col_count:
                diag_contents.append(matrix[row][col])
        yield diag_contents

if __name__ == "__main__":
    file_name = 'adventofcode2024/day4puz1input.txt'

    data_matrix = [];

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            data_matrix.append(line.strip())

    find_count = 0
    for row in data_matrix:
        find_count += find_xmas(row)
    
    for col in transpose(data_matrix):
        find_count += find_xmas(col)

    for diag in generate_diagonals(data_matrix):
        find_count += find_xmas(diag)
        
    print()
    print(find_count)
    
