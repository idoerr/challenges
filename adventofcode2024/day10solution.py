from collections import defaultdict
import itertools

def follow_trails_recurse(trail_matrix, row, col, target_height):

    # handle out-of-bounds cases
    if row < 0 or row >= len(trail_matrix):
        return (0, set())
    
    if col < 0 or col >= len(trail_matrix[0]):
        return (0, set())

    cur_height = trail_matrix[row][col]

    # return 0 if the target height is not the current height
    if target_height != cur_height:
        return (0, set())

    # base case: at the end of the trail
    if cur_height == 9:
        ret_set = set()
        ret_set.add((row, col))
        return (1, ret_set)
    
    new_target_height = cur_height + 1
    total_trails = 0
    final_destinations = set()

    # print(row, col, cur_height)

    # recursion cases, check all adjacent cells.
    trail_count, dest_set = follow_trails_recurse(trail_matrix, row - 1, col, new_target_height)
    total_trails += trail_count
    final_destinations = final_destinations.union(dest_set)

    trail_count, dest_set = follow_trails_recurse(trail_matrix, row, col - 1, new_target_height)
    total_trails += trail_count
    final_destinations = final_destinations.union(dest_set)

    trail_count, dest_set = follow_trails_recurse(trail_matrix, row + 1, col, new_target_height)
    total_trails += trail_count
    final_destinations = final_destinations.union(dest_set)

    trail_count, dest_set = follow_trails_recurse(trail_matrix, row, col + 1, new_target_height)
    total_trails += trail_count
    final_destinations = final_destinations.union(dest_set)

    return total_trails, final_destinations


if __name__ == "__main__":
    file_name = 'adventofcode2024/day10input.txt'

    data_matrix = []

    row = 0
    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            data_matrix.append(list(map(int, line.strip())))

    end_rating = 0
    end_score = 0

    for row_index, row in enumerate(data_matrix):
        for col_index, col in enumerate(row):
            if col == 0:
                total_trails, end_dests = follow_trails_recurse(data_matrix, row_index, col_index, 0)
                end_rating += total_trails
                end_score += len(end_dests)

    print("Final Score: " + str(end_score))
    print("Final Rating: " + str(end_rating))
    
