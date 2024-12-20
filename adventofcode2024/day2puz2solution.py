from collections import defaultdict

if __name__ == "__main__":
    file_name = 'adventofcode2024/day2puz1input.txt'

    safe_count = 0

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            invalid_count = 0
            report_numbers = list(map(int, line.split(' ')))

            direction = 0

            for a, b in zip(report_numbers, report_numbers[1:]):
                delta = b - a
                delta_abs = abs(delta)
                if delta_abs < 1 or delta_abs > 3:
                    invalid_count += 1
                    continue
                
                delta_dir = delta / delta_abs
                if direction == 0:
                    direction = delta_dir
                elif direction != delta_dir:
                    invalid_count += 1
                    continue

            if invalid_count < 2:
                safe_count += 1

    print(safe_count)
