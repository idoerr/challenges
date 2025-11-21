from collections import defaultdict
import itertools

def find_area_and_perimeter_using_fill_algorithm(data_matrix, visit_matrix, row, col):

    if visit_matrix[row][col]:
        return None
    
    fill_value = data_matrix[row][col]

    area_count = 0
    perimeter_count = 0

    visit_queue = []
    visit_queue.append((row, col))

    fill_cells = []

    # Perform the fill algorithm
    while len(visit_queue) > 0:
        visit_row, visit_col = visit_queue.pop()

        if visit_matrix[visit_row][visit_col]:
            continue

        visit_matrix[visit_row][visit_col] = True
        fill_cells.append((visit_row, visit_col))

        area_count += 1

        cur_perimeter_count = 0

        # Handle top
        if visit_row == 0:
            cur_perimeter_count += 1
        elif data_matrix[visit_row - 1][visit_col] == fill_value:
            new_cell = (visit_row - 1, visit_col)
            if not visit_matrix[new_cell[0]][new_cell[1]]:
                visit_queue.append(new_cell)
        else:
            cur_perimeter_count += 1

        # Handle left
        if visit_col == 0:
            cur_perimeter_count += 1
        elif data_matrix[visit_row][visit_col - 1] == fill_value:
            new_cell = (visit_row, visit_col - 1)
            if not visit_matrix[new_cell[0]][new_cell[1]]:
                visit_queue.append(new_cell)
        else:
            cur_perimeter_count += 1

        # Handle bottom
        if visit_row + 1 == len(data_matrix):
            cur_perimeter_count += 1
        elif data_matrix[visit_row + 1][visit_col] == fill_value:
            new_cell = (visit_row + 1, visit_col)
            if not visit_matrix[new_cell[0]][new_cell[1]]:
                visit_queue.append(new_cell)
        else:
            cur_perimeter_count += 1

        # Handle right
        if visit_col + 1 == len(data_matrix[visit_row]):
            cur_perimeter_count += 1
        elif data_matrix[visit_row][visit_col + 1] == fill_value:
            new_cell = (visit_row, visit_col + 1)
            if not visit_matrix[new_cell[0]][new_cell[1]]:
                visit_queue.append(new_cell)
        else:
            cur_perimeter_count += 1

        perimeter_count += cur_perimeter_count
    
    return area_count, perimeter_count, fill_cells

def find_fence_segment_count(cell_list):

    cell_set = set()

    for cell in cell_list:
        cell_set.add(cell)

    cells_with_top_fence_grouped_by_row = defaultdict(list)
    cells_with_bottom_fence_grouped_by_row = defaultdict(list)
    cells_with_left_fence_grouped_by_column = defaultdict(list)
    cells_with_right_fence_grouped_by_column = defaultdict(list)

    for cell in cell_list:
        row, col = cell
        
        if (row - 1, col) not in cell_set:
            cells_with_top_fence_grouped_by_row[row].append(col)
        
        if (row + 1, col) not in cell_set:
            cells_with_bottom_fence_grouped_by_row[row].append(col)

        if (row, col - 1) not in cell_set:
            cells_with_left_fence_grouped_by_column[col].append(row)

        if (row, col + 1) not in cell_set:
            cells_with_right_fence_grouped_by_column[col].append(row)

    total_segment_count = 0
    
    total_segment_count += count_segments_in_grouped_cell_map(cells_with_top_fence_grouped_by_row, "Top")
    total_segment_count += count_segments_in_grouped_cell_map(cells_with_bottom_fence_grouped_by_row, "Bottom")
    total_segment_count += count_segments_in_grouped_cell_map(cells_with_left_fence_grouped_by_column, "Left")
    total_segment_count += count_segments_in_grouped_cell_map(cells_with_right_fence_grouped_by_column, "Right")

    return total_segment_count

def count_segments_in_grouped_cell_map(grouped_cell_map, side):
    segment_count = 0
    # Handle Top fences
    for first_coord in grouped_cell_map.keys():
        prev_coord = -5
        for second_coord in sorted(grouped_cell_map[first_coord]):
            if prev_coord != second_coord - 1:
                segment_count += 1
            prev_coord = second_coord
    # print(side, segment_count, grouped_cell_map)
    return segment_count


if __name__ == "__main__":
    file_name = 'adventofcode2024/day12input.txt'

    data_matrix = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(list(line.strip()))

    col_count = len(data_matrix[0])
    visit_matrix = []
    for row in data_matrix:
        visit_matrix.append([False] * col_count)

    region_results = []

    for row_index, row in enumerate(data_matrix):
        for col_index, col in enumerate(row):
            found_stats = find_area_and_perimeter_using_fill_algorithm(data_matrix, visit_matrix, row_index, col_index)
            if found_stats is not None:
                area, perimeter, fill_cells = found_stats

                segment_count = find_fence_segment_count(fill_cells)
                region_results.append((area, perimeter, segment_count))
    
    total_part_1 = 0
    total_part_2 = 0
    
    for region_area, region_perimeter, region_segments in region_results:
        # print(region_area, region_perimeter, region_area * region_perimeter, region_segments)
        total_part_1 += region_area * region_perimeter
        total_part_2 += region_area * region_segments
    print(total_part_1)
    print(total_part_2)
    
