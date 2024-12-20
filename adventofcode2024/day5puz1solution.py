from collections import defaultdict
from itertools import combinations
import math

if __name__ == "__main__":
    file_name = 'adventofcode2024/day5puz1input.txt'

    sort_ordering = defaultdict(list)
    test_lists = []

    parse_ordering = True

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            if line.strip() == '':
                parse_ordering = False
                continue

            if parse_ordering:
                left, right = line.split('|', 2)
                sort_ordering[int(left)].append(int(right))
            else:
                test_lists.append(list(map(int, line.split(','))))
            
    valid_ordering_count = 0
    middle_pages_sum = 0
    for test_pages in test_lists:
        valid_ordering = True
        for a, b in combinations(test_pages, 2):
            
            enforce_before = sort_ordering[b]
            if a in enforce_before:
                valid_ordering = False
                break
        if valid_ordering:
            valid_ordering_count += 1
            middle_pages_sum += test_pages[math.floor(len(test_pages) / 2.0)]
    
    print()
    print(valid_ordering_count)
    print(middle_pages_sum)
