from functools import reduce
import math

def point_distance(a, b):
    x_distance = (a[0] - b[0]) ** 2
    y_distance = (a[1] - b[1]) ** 2
    z_distance = (a[2] - b[2]) ** 2
    return math.sqrt(x_distance + y_distance + z_distance)

def calc_distance_between_points(point_list):
    
    point_distance_list = []

    for i, first_point in enumerate(point_list[:-1]):
        for second_point in point_list[i+1:]:
            distance_between = point_distance(first_point, second_point)

            point_distance_list.append((distance_between, first_point, second_point))
    
    return sorted(point_distance_list)

def find_circuit(circuit_list, point):
    for circuit in circuit_list:
        if point in circuit:
            return circuit
    return None

def build_circuit_list(distance_points, distinct_point_count, build_count=None):

    circuit_list = []
    circuit_joins = []

    if build_count is None:
        build_count = len(distance_points)

    for i in range(build_count):
        distance, first_point, second_point = distance_points[i]

        first_point_circuit = find_circuit(circuit_list, first_point)
        second_point_circuit = find_circuit(circuit_list, second_point)

        circuit_joins.append((first_point, second_point))

        if first_point_circuit is None and second_point_circuit is None:
            new_circuit = set()
            new_circuit.add(first_point)
            new_circuit.add(second_point)
            circuit_list.append(new_circuit)
        elif first_point_circuit is None:
            second_point_circuit.add(first_point)
        elif second_point_circuit is None:
            first_point_circuit.add(second_point)
        elif first_point_circuit == second_point_circuit:
            # Do Nothing
            pass
        else:
            new_circuit = first_point_circuit.union(second_point_circuit)
            circuit_list.remove(first_point_circuit)
            circuit_list.remove(second_point_circuit)
            circuit_list.append(new_circuit)

        if len(circuit_list) == 1 and len(circuit_list[0]) == distinct_point_count:
            break
    return circuit_list, circuit_joins

if __name__ == '__main__':
    file_name = 'adventofcode2025/day8input.txt'

    point_list = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            x, y, z = line.split(',')
            point = (int(x), int(y), int(z))
            point_list.append(point)

    distinct_point_count = len(point_list)
    points_with_distance = calc_distance_between_points(point_list)

    # Part 1
    circuits, add_order = build_circuit_list(points_with_distance,distinct_point_count, 1000)
    circuit_lens = sorted(map(len, circuits), reverse=True)
    circuit_top_3_mult = reduce(lambda out, x: out * x, circuit_lens[:3], 1)
    print(circuit_top_3_mult)

    # Part 2
    circuits, add_order = build_circuit_list(points_with_distance, distinct_point_count)
    final_first_point, final_second_point = add_order[-1]
    print(final_first_point[0] * final_second_point[0])