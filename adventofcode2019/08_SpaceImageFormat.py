
from collections import defaultdict

input_file = 'adventofcode2019/08_SpaceImageFormat.txt'
# input_file = '02_ProgramAlarm.txt'

def freq_count(coll):
    freq_dict = defaultdict(int)

    for x in coll:
        freq_dict[x] += 1
    
    return freq_dict

if __name__ == '__main__':

    file_obj = open(input_file, 'r')

    input_str = file_obj.readline().strip()

    num_map = list(map(int, input_str))

    image_width = 25
    image_height = 6
    layer_size = image_width * image_height

    layers = []
    for layer_start in range(0, len(num_map), layer_size):
        layers.append(num_map[layer_start: layer_start + layer_size])

    print("Part 1 Result")
    layer_freq_map = map(freq_count, layers)

    min_freq_dict = min(layer_freq_map, key=lambda f: f[0])

    print(min_freq_dict)
    print(min_freq_dict[1] * min_freq_dict[2])

    print()
    print("Part 2 Result")

    result_arr = [2] * layer_size

    for layer_data in layers:
        for i in range(layer_size):
            if result_arr[i] == 2:
                result_arr[i] = layer_data[i]
    
    for row in range(image_height):
        start_index = row * image_width
        end_index = (row + 1) * image_width
        print(result_arr[start_index:end_index])
