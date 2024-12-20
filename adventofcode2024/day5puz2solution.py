from collections import defaultdict
import math
import functools

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

    def comparator(item1, item2):
        enforce_before = sort_ordering[item1]
        if item2 in enforce_before:
            return -1
        
        enforce_before = sort_ordering[item2]
        if item1 in enforce_before:
            return 1
        
        return 0
            
    valid_ordering_count = 0
    middle_pages_sum = 0

    incorrect_ordering_count = 0
    incorrect_middle_pages_sum = 0
    for test_pages in test_lists:
        
        sorted_pages = sorted(test_pages, key=functools.cmp_to_key(comparator))
        middle_page = sorted_pages[math.floor(len(test_pages) / 2.0)]

        if sorted_pages == test_pages:
            middle_pages_sum += middle_page
            valid_ordering_count += 1
        else:
            incorrect_ordering_count += 1
            incorrect_middle_pages_sum += middle_page

    
    print()
    print(valid_ordering_count)
    print(middle_pages_sum)
    print(incorrect_ordering_count)
    print(incorrect_middle_pages_sum)

    