
def try_read_val(data_matrix, i_row, i_col):
    if i_row < 0 or i_row >= len(data_matrix):
        return 0
    if i_col < 0 or i_col >= len(data_matrix[i_row]):
        return 0

    return data_matrix[i_row][i_col]

def count_neighbours(data_matrix):

    ret_matrix = []

    for i_row, row in enumerate(data_matrix):
        ret_row = []
        ret_matrix.append(ret_row)
        for i_col, val in enumerate(row):

            cell_neighbour_count = 0
            cell_neighbour_count += try_read_val(data_matrix, i_row - 1, i_col - 1)
            cell_neighbour_count += try_read_val(data_matrix, i_row - 1, i_col)
            cell_neighbour_count += try_read_val(data_matrix, i_row - 1, i_col + 1)
            cell_neighbour_count += try_read_val(data_matrix, i_row, i_col - 1)
            cell_neighbour_count += try_read_val(data_matrix, i_row, i_col + 1)
            cell_neighbour_count += try_read_val(data_matrix, i_row + 1, i_col - 1)
            cell_neighbour_count += try_read_val(data_matrix, i_row + 1, i_col)
            cell_neighbour_count += try_read_val(data_matrix, i_row + 1, i_col + 1)
            
            ret_row.append(cell_neighbour_count)

    return ret_matrix

def remove_1_from_neighbours(neighbour_matrix, remove_location):
    remove_row, remove_col = remove_location

    try_subtract_val_in_matrix(neighbour_matrix, remove_row - 1, remove_col - 1, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row - 1, remove_col, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row - 1, remove_col + 1, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row, remove_col - 1, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row, remove_col + 1, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row + 1, remove_col - 1, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row + 1, remove_col, 1)
    try_subtract_val_in_matrix(neighbour_matrix, remove_row + 1, remove_col + 1, 1)

def try_subtract_val_in_matrix(data_matrix, i_row, i_col, col):
    if i_row < 0 or i_row >= len(data_matrix):
        return
    if i_col < 0 or i_col >= len(data_matrix[i_row]):
        return

    data_matrix[i_row][i_col] -= 1

if __name__ == '__main__':
    file_name = 'adventofcode2025/day4input.txt'

    paper_roll_matrix = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            paper_roll_matrix.append(list(map(lambda x: 1 if x == '@' else 0, line.strip())))

    roll_neighbour_matrix = count_neighbours(paper_roll_matrix)

    

    removable_count = 0
    is_first_iter = True

    while True:
        flat_roll_matrix = [cell for row in paper_roll_matrix for cell in row]
        flat_neighbour_matrix_with_indexes = [((i_row, i_col), cell) for i_row, row in enumerate(roll_neighbour_matrix) for i_col, cell in enumerate(row)]

        less_than_4_neighbour_filter = filter(lambda x: x[0] == 1 and x[1][1] < 4, zip(flat_roll_matrix, flat_neighbour_matrix_with_indexes))
        less_than_4_neighbour_indexes = map( lambda x: x[1][0], less_than_4_neighbour_filter)

        removable_this_iter = 0
        for remove_cell in less_than_4_neighbour_indexes:
            remove_row, remove_col = remove_cell
            paper_roll_matrix[remove_row][remove_col] = 0

            remove_1_from_neighbours(roll_neighbour_matrix, remove_cell)

            removable_this_iter += 1

        removable_count += removable_this_iter

        if is_first_iter:
            print(removable_this_iter)
            is_first_iter = False

        

        if removable_this_iter == 0:
            break

    print(removable_count)