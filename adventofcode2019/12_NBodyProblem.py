
from functools import reduce
import itertools

class Moon:

    def __init__(self, x: int, y: int, z: int):
        self.orig_postion = (x,y,z)
        self.orig_velocity = (0,0,0)
        self.position = [x,y,z]
        self.velocity = [0,0,0]
    
    def reset(self):
        self.position = list(self.orig_postion)
        self.velocity = list(self.orig_velocity)

    def move(self):
        for i in range(len(self.position)):
            self.dimension_move(i)
    
    def dimension_move(self, index):
        self.position[index] += self.velocity[index]
    
    def dimension_vals(self, index):
        return (self.position[index], self.velocity[index])
    
    def energy(self):
        position_sum = sum(map(abs, self.position))
        velocity_sum = sum(map(abs, self.velocity))

        return position_sum * velocity_sum
    
    def apply_gravity(self, other):
        for i in range(len(self.position)):
            self.apply_gravity_index(other, i)

    def apply_gravity_index(self, other, index):
        delta_pos = other.position[index] - self.position[index]
        if delta_pos != 0:
            self.velocity[index] += delta_pos / abs(delta_pos)
        
    def __repr__(self):
        return str((self.position, self.velocity))

def moon_step(moon_arr):

    for i, first_moon in enumerate(moon_arr[0:-1]):
        for second_moon in moon_arr[i+1:]:
            first_moon.apply_gravity(second_moon)
            second_moon.apply_gravity(first_moon)
    
    for moon in moon_arr:
        moon.move()

def arr_dim_moon_state(moon_arr, index):
    return tuple(x.dimension_vals(index) for x in moon_arr)

def dim_moon_step(moon_arr, index):

    for first_moon, second_moon in itertools.combinations(moon_arr, 2):
        first_moon.apply_gravity_index(second_moon, index)
        second_moon.apply_gravity_index(first_moon, index)
    
    for moon in moon_arr:
        moon.dimension_move(index)


def find_dimension_loop(moon_arr, index):

    step_dict = {}
    count = 0

    max_count = 1000000

    while count < max_count:
        cur_state = arr_dim_moon_state(moon_arr, index)
        if cur_state in step_dict:
            break
        
        step_dict[cur_state] = count
        count += 1

        dim_moon_step(moon_arr, index)
    
    cur_state = arr_dim_moon_state(moon_arr, index)
    if cur_state not in step_dict:
        raise ValueError("Did not find cycle in %d steps" % max_count)
    orig_count = step_dict[cur_state]

    return count - orig_count, orig_count

def lcm(a, b):
    cur_gcd = gcd(a, b)
    new_a = a / cur_gcd
    return new_a * b

def gcd(a, b):

    if b > a:
        return gcd(b, a)
    if b == 0:
        return a
    
    return gcd(b, a % b)

input_file = 'adventofcode2019/12_NBodyProblem.txt'

if __name__ == "__main__":

    file_obj = open(input_file, 'r')

    moon_arr = []

    for moon_coords in file_obj.readlines():
        moon_coords = moon_coords.strip()

        # take off outer < >
        moon_coords = moon_coords[1:-1]
        coord_arr = moon_coords.split(",")

        coord_dict = {}

        for coord in coord_arr:
            coord = coord.strip()
            c_ref, c_val = coord.split("=")
            c_val = int(c_val)
            coord_dict[c_ref] = c_val
        
        moon_obj = Moon(**coord_dict)
        moon_arr.append(moon_obj)
    
    for i in range(1, 1001):
        moon_step(moon_arr)
        if i % 100 == 0:
            print(i, sum(map(Moon.energy, moon_arr)))
    
    print("Part 1 Result")
    print(moon_arr)
    print(sum(map(Moon.energy, moon_arr)))

    for moon in moon_arr:
        moon.reset()
    
    print()
    print("Part 2 Result")

    loop_lengths = []
    loop_offsets = []
    
    for i in range(3):
        loop_len, loop_off = find_dimension_loop(moon_arr, i)
        print((loop_len, loop_off))
        loop_lengths.append(loop_len)
        loop_offsets.append(loop_off)
    
    lengths_gcd = int(reduce(gcd, loop_lengths))
    
    total_len = reduce(lcm, loop_lengths)
    max_offset = max(loop_offsets)
    print(total_len + max_offset)
