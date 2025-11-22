import math

def calculate_min_token_cost_iter(a_val, a_cost, b_val, b_cost, prize_loc):

    a_x, a_y = a_val
    b_x, b_y = b_val
    loc_x, loc_y = prize_loc

    min_token_cost = 999999
    min_a_presses = -1
    min_b_presses = -1
    for a_presses in range(101):
        a_x_mult = a_x * a_presses
        a_y_mult = a_y * a_presses

        loc_x_remain = loc_x - a_x_mult
        loc_y_remain = loc_y - a_y_mult

        if loc_x_remain < 0 or loc_y_remain < 0:
            break

        if loc_x_remain % b_x == 0 and loc_y_remain % b_y == 0:
            b_x_presses = loc_x_remain // b_x
            b_y_presses = loc_y_remain // b_y

            if b_x_presses != b_y_presses:
                continue
            
            token_cost = a_presses * a_cost + b_x_presses * b_cost

            if token_cost < min_token_cost:
                min_token_cost = token_cost
                min_a_presses = a_presses
                min_b_presses = b_x_presses
    
    return min_a_presses, min_b_presses, min_token_cost

def gcd(a, b):

    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    
    return gcd(b, a % b)

# developed based on wikipedia pseudo-code
def extended_gcd(a, b):
    prev_r = a
    cur_r = b
    prev_s = 1
    cur_s = 0
    prev_t = 0
    cur_t = 1

    while cur_r != 0:
        quotient = prev_r // cur_r

        temp_r = cur_r
        cur_r = prev_r - quotient * cur_r
        prev_r = temp_r

        temp_s = cur_s
        cur_s = prev_s - quotient * cur_s
        prev_s = temp_s

        temp_t = cur_t
        cur_t = prev_t - quotient * cur_t
        prev_t = temp_t

    # print("Bezout coefficients:", prev_s, prev_t)
    # print("gcd:", prev_r)
    # print("quotients by the gcd:", cur_t, cur_s)

    return prev_r, prev_s, prev_t

def calculate_possible_token_sets_for_axis(a, b, target):
    # We are calculating possible solutions using the diophantine equation ax + by = c
    # We will need to calculate the shape of infinite solutions using the extended euclidian algorithm
    # Then, we will look for set of solutions where both a and b are positive.

    gcd, a_mult, b_mult = extended_gcd(a, b)

    if target % gcd != 0:
        return None
    
    multiplier = target // gcd

    solution_a = a_mult * multiplier
    solution_b = b_mult * multiplier

    step_a = -b // gcd
    step_b = a // gcd

    # We want both numbers to be positive, and there are a limited number of solutions where this is true
    # Calculate the bounds between these two points, by calculating when a_x_zero and b_x_zero go negative.
    a_zero = -solution_a // step_a
    b_zero = -solution_b // step_b + 1 # This will calculate the last negative number if not incremented by one

    first_solution_a = solution_a + b_zero * step_a
    first_solution_b = solution_b + b_zero * step_b

    number_valid_steps = a_zero - b_zero

    return number_valid_steps, first_solution_a, first_solution_b, step_a, step_b

def calculate_min_token_cost_algebra(a_val, a_cost, b_val, b_cost, prize_loc):

    a_x, a_y = a_val
    b_x, b_y = b_val
    loc_x, loc_y = prize_loc

    # Perform token calculations for both axes.
    x_axis_calcs = calculate_possible_token_sets_for_axis(a_x, b_x, loc_x)
    y_axis_calcs = calculate_possible_token_sets_for_axis(a_y, b_y, loc_y)

    if x_axis_calcs is None or y_axis_calcs is None:
        return -1, -1, None

    max_steps_x, start_a_x, start_b_x, step_a_x, step_b_x = x_axis_calcs
    max_steps_y, start_a_y, start_b_y, step_a_y, step_b_y = y_axis_calcs

    # Using y = mx + b, we can construct 4 equations using these variables
    # (Changing y for n to reduce confusion)
    # Note that step_x and step_y are unknown values that we will need to solve for
    # n(a) = step_a_x * step_x + start_a_x
    # n(a) = step_a_y * step_y + start_a_y
    # n(b) = step_b_x * step_x + start_b_x
    # n(b) = step_b_y * step_y + start_b_y
    # 
    # Since we want n to be the same number for a and b, we can set them equal to each other
    # step_a_x * step_x + start_a_x = step_a_y * step_y + start_a_y
    # step_b_x * step_x + start_b_x = step_b_y * step_y + start_b_y
    # 
    # Now we can solve equation 1 for step_x
    # step_x = (step_a_y * step_y + start_a_y - start_a_x) / step_a_x
    # 
    # Substitute step_x into equation 2, then solve for step_y
    # step_b_x * (step_a_y * step_y + start_a_y - start_a_x) / step_a_x + start_b_x = step_b_y * step_y + start_b_y
    # (step_b_x * step_a_y / step_a_x) * step_y - step_b_y * step_y = start_b_y - start_b_x - step_b_x / step_a_x * (start_a_y - start_a_x)
    # (step_b_x * step_a_y - step_b_y * step_a_x) * step_y / step_a_x
    # step_y = step_a_x * (start_b_y - start_b_x - step_b_x / step_a_x * (start_a_y - start_a_x)) / (step_b_x * step_a_y - step_b_y * step_a_x)
    step_y = step_a_x * (start_b_y - start_b_x - step_b_x / step_a_x * (start_a_y - start_a_x)) / (step_b_x * step_a_y - step_b_y * step_a_x)
    step_y = round(step_y, 4) # get around floating-point precision
    
    # We can only take an integer number of steps, so ignore solutions that cannot.
    if not step_y.is_integer():
        print(step_y)
        return -1, -1, None
    
    result_a = int(step_a_y * step_y + start_a_y)
    result_b = int(step_b_y * step_y + start_b_y)

    end_cost = result_a * a_cost + result_b * b_cost

    return result_a, result_b, end_cost

if __name__ == "__main__":
    file_name = 'adventofcode2024/day13input.txt'

    data_matrix = []

    button_a_vals = []
    button_b_vals = []
    prizes = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            if line.strip() == "":
                continue

            label, values = line.split(':')
            x, y = values.split(',')
            x_val = int(x.strip()[2:])
            y_val = int(y.strip()[2:])
            if label == 'Button A':
                button_a_vals.append((x_val, y_val))
            elif label == 'Button B':
                button_b_vals.append((x_val, y_val))
            elif label == 'Prize':
                prizes.append((x_val, y_val))

    button_a_cost = 3
    button_b_cost = 1

    total_min_cost = 0
    total_part_2_min_cost = 0

    for button_a, button_b, prize_loc in zip(button_a_vals, button_b_vals, prizes):
        # calculate for part 1
        a_presses, b_presses, min_cost = calculate_min_token_cost_algebra(button_a, button_a_cost, button_b, button_b_cost, prize_loc)
        if a_presses != -1:
            total_min_cost += min_cost

        # calculate for part 1
        new_prize_loc = 10000000000000 + prize_loc[0], 10000000000000 + prize_loc[1]
        a_presses, b_presses, min_cost = calculate_min_token_cost_algebra(button_a, button_a_cost, button_b, button_b_cost, new_prize_loc)
        if a_presses != -1:
            total_part_2_min_cost += min_cost
    
    print(total_min_cost)
    print(total_part_2_min_cost)