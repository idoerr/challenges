

def find_cross_mas( matrix ):

    find_count = 0

    # iterate over the matrix, ignoring the border, as an A on the border is useless.
    for row in range(1, len(matrix) - 1):
        for col in range(1, len(matrix[0]) - 1):
            # Search for an A first
            if matrix[row][col] == 'A':
                # check the southeast diagonal for M and S, in either order
                if matrix[row-1][col-1] == 'M' and matrix[row+1][col+1] == 'S':
                    pass
                elif matrix[row-1][col-1] == 'S' and matrix[row+1][col+1] == 'M':
                    pass
                else:
                    continue
                # check the southwest diagonal for M and S
                if matrix[row+1][col-1] == 'M' and matrix[row-1][col+1] == 'S':
                    pass
                elif matrix[row+1][col-1] == 'S' and matrix[row-1][col+1] == 'M':
                    pass
                else:
                    continue

                # if we passed those checks, then continue
                find_count += 1

    return find_count


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

if __name__ == "__main__":
    file_name = 'adventofcode2024/day4puz1input.txt'

    data_matrix = [];

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            data_matrix.append(line.strip())

    find_result = find_cross_mas(data_matrix)
    print()
    print(find_result)
    
