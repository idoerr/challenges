import re
import functools

def calc_possible_distances( total_time ):
    total_distances = []

    for hold_down_time in range(1, total_time):
        distance_travel = hold_down_time * (total_time - hold_down_time)
        total_distances.append(distance_travel)

    return total_distances

if __name__ == "__main__":
    file_name = 'adventofcode2023/day6puz2input.txt'

    ways_to_win = [1]

    with open(file_name, 'r') as file_handle:
        times_str = file_handle.readline().split(':', 1)[1]
        race_time = int(times_str.replace(' ', ''))
        
        distance_str = file_handle.readline().split(':', 1)[1]
        race_distance = int(distance_str.replace(' ', ''))
        
        possible_distances = calc_possible_distances(race_time)

        winning_distances = [ x for x in possible_distances if x > race_distance ]

        ways_to_win.append(len(winning_distances))
    print()
    print(ways_to_win)
    print( functools.reduce( lambda a, b: a*b, ways_to_win ) )




