
def rocket_calc(val: int) -> int:
    ret_val = val // 3 - 2
    return ret_val if ret_val >= 0 else 0

def rocket_fuel_calc(val: int) -> int:
    ret_val = 0

    while val > 0:
        val = rocket_calc(val)
        ret_val += val
    
    return ret_val

input_file = 'adventofcode2019/01_RocketEquation.txt'

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    input_arr = file_obj.readlines()

    input_arr = list(map(int, input_arr))

    output_calc = map(rocket_calc, input_arr)

    print("Part 1 Result")
    print(sum(output_calc))
    print()

    output_calc = map(rocket_fuel_calc, input_arr)

    print("Part 2 Result")
    print(sum(output_calc))
    

