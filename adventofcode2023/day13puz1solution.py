
def rotate_matrix(matrix):
    new_matrix = []

    for i in range(len(matrix[0])):
        new_row = ''
        for row in matrix:
            cell = row[i]
            new_row += cell
        new_matrix.append(new_row)
    
    return new_matrix

def find_reflection(matrix):
    
    hash_rows = []
    for x in matrix:
        hash_rows.append(hash(x))
    
    for divide_index in range(1, len(matrix)):
        top_section = hash_rows[0:divide_index]
        bot_section = hash_rows[divide_index:]

        not_equal_found = False
        for top_row, bot_row in zip(reversed(top_section), bot_section):
            if top_row != bot_row:
                not_equal_found = True
                break
        
        if not not_equal_found:
            return divide_index
    
    return -1


if __name__ == "__main__":
    file_name = 'adventofcode2023/day13puz1input.txt'

    matrix_list = [];
    current_matrix = [];

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            line = line.strip()
            if line == '':
                if len(current_matrix) > 0:
                    matrix_list.append(current_matrix)
                current_matrix = []
            else:
                current_matrix.append(line)
        
        if len(current_matrix) > 0:
            matrix_list.append(current_matrix)

    matrix_reflection_nums = []

    for matrix in matrix_list:

        horizontal_reflection = find_reflection(matrix)
        vertical_reflection = find_reflection(rotate_matrix(matrix))

        reflection_no = 0

        if vertical_reflection != -1:
            reflection_no += vertical_reflection
        if horizontal_reflection != -1:
            reflection_no += 100 * horizontal_reflection

        if reflection_no == 0:
            print()
            for row in matrix:
                print(row)
        
        matrix_reflection_nums.append(reflection_no)
    
    print()
    print(sum(matrix_reflection_nums))

