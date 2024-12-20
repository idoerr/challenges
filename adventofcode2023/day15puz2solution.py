from collections import defaultdict

def hash_str(to_hash):
    cur_hash = 0
    for x in to_hash:
        cur_hash = ((cur_hash + ord(x)) * 17) % 256
    return cur_hash

def find_in_box(box, search_str):
    for i, x in enumerate(box):
        key_str, focal_val = x

        if key_str == search_str:
            return i
    return -1

if __name__ == "__main__":
    file_name = 'adventofcode2023/day15puz1input.txt'

    boxes = defaultdict(list)

    with open(file_name, 'r') as file_handle:
        data = file_handle.read()
        data = data.replace('\n', '')
        
        instruction_arr = data.split(',')
        for instruction in instruction_arr:
            if instruction[-1] == '-':
                key_str = instruction[0:-1]
            else:
                key_str = instruction[0:-2]
            key_hash = hash_str(key_str)

            box = boxes[key_hash]

            if instruction[-1] == '-':
                del_index = find_in_box(box, key_str)

                if del_index != -1:
                    box.pop(del_index)
            elif instruction[-2] == '=':
                focal_value = int(instruction[-1])
                find_index = find_in_box(box, key_str)

                if find_index == -1:
                    box.append((key_str, focal_value))
                else:
                    box[find_index] = (key_str, focal_value)
    
    total_focusing_power = 0
    print('k')

    for box_num, box in boxes.items():

        for slot_num, x in enumerate(box):
            key_str, focal_value = x

            focusing_power = (box_num + 1) * (slot_num + 1) * focal_value

            total_focusing_power += focusing_power

    print(total_focusing_power)
