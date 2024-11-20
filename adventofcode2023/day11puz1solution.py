import re

if __name__ == "__main__":
    file_name = 'adventofcode2023/day11puz1input.txt'

    orig_matrix = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            orig_matrix.append(line.strip())

    mod_matrix = []
    # duplicate rows with '#'
    for row in orig_matrix:
        if row.find('#') == -1:
            mod_matrix.append(row)
            mod_matrix.append(row)
        else:
            mod_matrix.append(row)

    cols_to_dup = []

    # find cols without '#'
    for i in range(len(mod_matrix[0])):
        found = False
        for row in mod_matrix:
            cell = row[i]
            if cell == '#':
                found = True
                break
        if not found:
            cols_to_dup.append(i)
    
    final_matrix = []

    #duplicate columns
    for row in mod_matrix:
        new_line = ''
        last_index = 0

        for i, cell in enumerate(row):
            if i in cols_to_dup:
                new_line += cell
                new_line += cell
            else:
                new_line += cell
        final_matrix.append(new_line)

    #find stars (#)
    star_locs = []
    for row_num, row in enumerate(final_matrix):
        for match in re.finditer('#', row):
            star_locs.append((row_num, match.start(0)))

    #calculate distances between star pairs
    distances_between_stars = []
    for i, star_1 in enumerate(star_locs):
        for star_2 in star_locs[i+1:]:
            total_delta = abs(star_2[0] - star_1[0]) + abs(star_2[1] - star_1[1])
            if star_1[0] == star_2[0] or star_1[1] == star_2[1]:
                distances_between_stars.append(total_delta)
            else:
                distances_between_stars.append(total_delta)
    


    print(sum(distances_between_stars))




