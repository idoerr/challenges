
import math

def calc_slope_between(first_asteroid, second_asteroid):
    delta_x = second_asteroid[0] - first_asteroid[0]
    delta_y = second_asteroid[1] - first_asteroid[1]

    if delta_x == 0:
        slope_x = 0
        slope_y = delta_y // abs(delta_y)
    elif delta_y == 0:
        slope_x = delta_x // abs(delta_x)
        slope_y = 0
    else:
        gcd_val = gcd(abs(delta_x), abs(delta_y))
        slope_x = delta_x // gcd_val
        slope_y = delta_y // gcd_val
    
    return (slope_x, slope_y)

def count_asteroids_between(asteroid_list, first_asteroid, second_asteroid):
    slope_x, slope_y = calc_slope_between(first_asteroid, second_asteroid)
    
    step_asteroid = (first_asteroid[0] + slope_x, first_asteroid[1] + slope_y)
    asteroid_count = 0
    
    while step_asteroid != second_asteroid:
        if tuple(step_asteroid) in asteroid_list:
            asteroid_count += 1

        step_asteroid = (step_asteroid[0] + slope_x, step_asteroid[1] + slope_y)
    
    return asteroid_count

def asteroid_visible(asteroid_list, first_asteroid, second_asteroid):
    return count_asteroids_between(asteroid_list, first_asteroid, second_asteroid) == 0

def calc_angle_between(asteroid_list, first_asteroid, second_asteroid):

    slope_x, slope_y = calc_slope_between(first_asteroid, second_asteroid)

    asteroids_between = count_asteroids_between(asteroid_list, first_asteroid, second_asteroid)

    hypoteneuse = math.sqrt(float(slope_x ** 2 + slope_y ** 2))
    divisor = abs(float(slope_x)) / hypoteneuse

    # Note:  straight up is the zero angle.  For this scenario, slope_y will be negative.
    # This means that the slope_y comparisons will be the opposite of expected.
    if slope_x == 0:
        if slope_y < 0:
            final_angle = 0
        else:
            final_angle = math.pi
    elif slope_y == 0:
        if slope_x < 0:
            final_angle = math.pi * 3 / 2
        else:
            final_angle = math.pi / 2
    elif slope_x > 0 and slope_y < 0:
        final_angle = math.asin(divisor)
    elif slope_x > 0 and slope_y > 0:
        final_angle = math.acos(divisor) + math.pi / 2
    elif slope_x < 0 and slope_y > 0:
        final_angle = math.asin(divisor) + math.pi
    elif slope_x < 0 and slope_y < 0:
        final_angle = math.acos(divisor) + math.pi * 3 / 2

    final_angle += asteroids_between * 2 * math.pi

    return final_angle

def gcd(a, b):

    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    
    return gcd(b, a % b)

input_file = 'adventofcode2019/10_MonitorStation.txt'

if __name__ == "__main__":

    file_obj = open(input_file, 'r')

    asteroid_list = {}

    for line_no, line in enumerate(file_obj.readlines()):
        line = line.strip()

        for i, x in enumerate(line):
            if x == "#":
                asteroid_list[(i, line_no)] = 0
    
    iter_asteroids = list(asteroid_list.keys())

    for ind, fir_ast in enumerate(iter_asteroids[0:-1]):
        for sec_ast in iter_asteroids[ind+1:]:

            if asteroid_visible(asteroid_list, fir_ast, sec_ast):
                asteroid_list[fir_ast] += 1
                asteroid_list[sec_ast] += 1
    
    max_ast = max(asteroid_list, key=lambda x: asteroid_list[x])

    print("Part 1 Result:")
    print(max_ast)
    print(asteroid_list[max_ast])

    print("Part 2 Result")
    
    angle_dict = {}

    for ast in iter_asteroids:
        if ast != max_ast:
            rotate_angle = calc_angle_between(asteroid_list, max_ast, ast)
        else:
            rotate_angle = -1

        angle_dict[ast] = rotate_angle

    angle_sorted = list(sorted(iter_asteroids, key=lambda x: angle_dict[x]))

    target_asteroid = angle_sorted[200]

    #print(target_asteroid)
    #print(angle_dict[target_asteroid])

    for i, x in enumerate(angle_sorted[1:]):
        print(i+1, x)
