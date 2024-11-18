
def get_next_number_recurse(num_arr):

    delta_arr = []

    for current, next in zip(num_arr, num_arr[1:]):
        delta_arr.append(next - current)
    
    if set(delta_arr) == {0}:
        return num_arr[-1]
    
    recurse_delta = get_next_number_recurse(delta_arr)

    return num_arr[-1] + recurse_delta


if __name__ == "__main__":
    file_name = 'adventofcode2023/day9puz1input.txt'

    next_numbers = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            number_arr = list(map(int, line.split(' ')))

            next_number = get_next_number_recurse(number_arr)

            next_numbers.append(next_number)

    print('k')
    print(sum(next_numbers))
