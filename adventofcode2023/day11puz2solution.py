import re
import bisect

if __name__ == "__main__":
    file_name = 'adventofcode2023/day11puz1input.txt'

    orig_matrix = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            orig_matrix.append(line.strip())

    rows_to_dup = []
    # duplicate rows with '#'
    for row_num, row in enumerate(orig_matrix):
        if row.find('#') == -1:
            rows_to_dup.append(row_num)

    cols_to_dup = []

    # find cols without '#'
    for i in range(len(orig_matrix[0])):
        found = False
        for row in orig_matrix:
            cell = row[i]
            if cell == '#':
                found = True
                break
        if not found:
            cols_to_dup.append(i)

    #find stars (#)
    star_locs = []
    for row_num, row in enumerate(orig_matrix):
        for match in re.finditer('#', row):
            star_locs.append((row_num, match.start(0)))

    #change coordinates based on missing columns
    mod_star_locs = []
    for star_loc in star_locs:
        mod_star_row = star_loc[0] + bisect.bisect(rows_to_dup, star_loc[0]) * 999999
        mod_star_col = star_loc[1] + bisect.bisect(cols_to_dup, star_loc[1]) * 999999
        mod_star_locs.append((mod_star_row, mod_star_col))

    #calculate distances between star pairs
    distances_between_stars = []
    for i, star_1 in enumerate(mod_star_locs):
        for star_2 in mod_star_locs[i+1:]:
            total_delta = abs(star_2[0] - star_1[0]) + abs(star_2[1] - star_1[1])
            if star_1[0] == star_2[0] or star_1[1] == star_2[1]:
                distances_between_stars.append(total_delta)
            else:
                distances_between_stars.append(total_delta)

    print(sum(distances_between_stars))
