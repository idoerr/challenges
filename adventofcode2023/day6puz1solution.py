import re
import functools

def calc_possible_distances( total_time ):
    total_distances = []

    for hold_down_time in range(1, total_time):
        distance_travel = hold_down_time * (total_time - hold_down_time)
        total_distances.append(distance_travel)

    return total_distances

if __name__ == "__main__":
    file_name = '2023/day6puz1input.txt'

    ways_to_win = [1]

    with open(file_name, 'r') as file_handle:
        times_str = file_handle.readline().split(':', 1)[1]
        race_times = list(map(int, re.findall('\d+', times_str)))
        
        distance_str = file_handle.readline().split(':', 1)[1]
        race_distances = list(map(int, re.findall('\d+', distance_str)))

        for i in range(len(race_times)):
            possible_distances = calc_possible_distances(race_times[i])

            winning_distances = [ x for x in possible_distances if x > race_distances[i] ]

            ways_to_win.append(len(winning_distances))
    print()
    print(ways_to_win)
    print( functools.reduce( lambda a, b: a*b, ways_to_win ) )




