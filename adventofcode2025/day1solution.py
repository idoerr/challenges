

if __name__ == '__main__':
    file_name = 'adventofcode2025/day1input.txt'

    dial_rotations = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            dial_rotations.append(line.strip())

    dial_0_count = 0
    dial_cross_0_count = 0
    current_dial_no = 50

    for rotations in dial_rotations:
        direction, distance = rotations[0], int(rotations[1:])

        dial_cross_0_count += distance // 100
        distance = distance % 100

        if direction == 'R':
            new_dial_no = current_dial_no + distance
        elif direction == 'L':
            new_dial_no = current_dial_no - distance
        
        if new_dial_no >= 100:
            dial_cross_0_count += 1
        elif current_dial_no != 0 and new_dial_no <= 0:
            dial_cross_0_count += 1

        current_dial_no = new_dial_no % 100

        if current_dial_no == 0:
            dial_0_count += 1
    
    print(dial_0_count)
    print(dial_cross_0_count)