from collections import defaultdict

def fire_tachyon_beam_into_splitters(splitter_set, max_rows, beam_start):

    first_row = beam_start[0]

    beam_set_by_row = defaultdict(lambda: defaultdict(int))
    beam_set_by_row[first_row][beam_start[1]] = 1

    split_count = 0

    for row in range(first_row, max_rows + 1):
        cur_row_beams = beam_set_by_row[row]
        next_row_beams = beam_set_by_row[row + 1]

        for beam_col, route_count in cur_row_beams.items():
            next_beam_loc = (row+1, beam_col)
            if next_beam_loc in splitter_set:
                next_row_beams[beam_col-1] += route_count
                next_row_beams[beam_col+1] += route_count
                split_count += 1
            else:
                next_row_beams[beam_col] += route_count
    
    last_row_beams = beam_set_by_row[max_rows]
    route_count = sum(last_row_beams.values())
    
    return split_count, route_count

if __name__ == '__main__':
    file_name = 'adventofcode2025/day7input.txt'

    row_count = 0
    start_beam = None
    splitter_set = set()

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            if line.find('S') != -1:
                start_beam = (row_count, line.find('S'))
            
            splitter_col = line.find('^')
            while splitter_col != -1:
                splitter_set.add((row_count, splitter_col))

                splitter_col = line.find('^', splitter_col + 1)
            
            row_count += 1

    split_count, route_count = fire_tachyon_beam_into_splitters(splitter_set, row_count, start_beam)

    print(split_count)
    print(route_count)

            