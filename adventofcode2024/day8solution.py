from collections import defaultdict
import itertools

if __name__ == "__main__":
    file_name = 'adventofcode2024/day8input.txt'

    data_matrix = []

    row = 0
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(list(line.strip()))

    # Extract the letter locations, and group by letter.
    letter_locations = defaultdict(list)

    for row_index, row in enumerate(data_matrix):
        for col_index, col in enumerate(row):
            if col != '.' and col != '#':
                letter_locations[col].append((row_index, col_index))

    def coord_subtract(a, b):
        return (a[0] - b[0], a[1] - b[1])
    def coord_add(a, b):
        return (a[0] + b[0], a[1] + b[1])

    def try_add_antinode(antinode_set, coord):
        if coord[0] < 0 or coord[0] >= len(data_matrix):
            return False
        if coord[1] < 0 or coord[1] >= len(data_matrix[0]):
            return False
        
        antinode_set.add(coord)
        return True

    antinode_locations_p1 = set()
    antinode_locations_p2 = set()

    for location_list in letter_locations.values():
        for a, b in itertools.combinations(location_list, 2):
            delta = coord_subtract(b, a)

            try_add_antinode(antinode_locations_p1, coord_add(b, delta))
            try_add_antinode(antinode_locations_p1, coord_subtract(a, delta))

            try_add_antinode(antinode_locations_p2, a)

            coord = a
            successful = True
            while successful:
                coord = coord_add(coord, delta)
                successful = try_add_antinode(antinode_locations_p2, coord)

            coord = a
            successful = True
            while successful:
                coord = coord_subtract(coord, delta)
                successful = try_add_antinode(antinode_locations_p2, coord)

    for coord in antinode_locations_p2:
        data_matrix[coord[0]][coord[1]] = '#'

    def pretty_print_matrix(matrix):
        for row in matrix:
            print(''.join(row))

    print()
    pretty_print_matrix(data_matrix)

    # print(antinode_locations)
    print()
    print(len(antinode_locations_p1))
    print(len(antinode_locations_p2))
    
