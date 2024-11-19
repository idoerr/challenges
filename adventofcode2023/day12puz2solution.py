
import datetime

# Using a dynamic programming approach
def find_valid_combo_count(needed_blocks, search_str, memo):
    
    process_result = -1
    if (needed_blocks, search_str) in memo:
        return memo[(needed_blocks), search_str]
    if len(needed_blocks) == 0:
        if len(search_str) == 0:
            process_result = 1
        if search_str.count('#') == 0:
            process_result = 1
        else:
            process_result = 0
    elif len(search_str) < len(needed_blocks[0]):
        process_result = 0
    else:
        first_block = needed_blocks[0]
        first_search_char = search_str[0]
        
        if first_search_char == '?':
            skip_search = find_valid_combo_count(needed_blocks, search_str[1:], memo)
            consume_search = 0

            if question_str_equals(search_str, first_block):
                consume_search = find_valid_combo_count(needed_blocks[1:], search_str[len(first_block):], memo)
            process_result = skip_search + consume_search
        elif first_search_char == '#':
            if question_str_equals(search_str, first_block):
                process_result = find_valid_combo_count(needed_blocks[1:], search_str[len(first_block):], memo)
            else:
                process_result = 0
        else:
            process_result = find_valid_combo_count(needed_blocks, search_str[1:], memo)
    
    memo[(needed_blocks, search_str)] = process_result
    return process_result
        
def question_str_equals(question_str, build_str):
    for a, b in zip(question_str, build_str):
        if a != '?' and a != b:
            return False
    return True

if __name__ == "__main__":
    file_name = 'adventofcode2023/day12puz2input.txt'
    print('k')

    start = datetime.datetime.now()

    row_valid_combinations = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            spring_layout, indexes = line.split(' ', 1)
            broken_spring_counts = list(map(int, indexes.split(',')))

            expanded_spring_layout = '?'.join([spring_layout] * 5)
            expanded_broken_spring_counts = broken_spring_counts * 5

            gen_spring_blocks = []
            for x in expanded_broken_spring_counts:
                gen_spring_blocks.append('#' * x + '.')
            gen_spring_blocks[-1] = gen_spring_blocks[-1][0:-1]
            gen_spring_blocks = tuple(gen_spring_blocks)

            valid_combinations = find_valid_combo_count(gen_spring_blocks, expanded_spring_layout, {})
            
            #print(2 ** spring_layout.count('?'), len(check_layouts), len(valid_layout))
            row_valid_combinations.append(valid_combinations)

    print('k')
    print(sum(row_valid_combinations))

    end = datetime.datetime.now()

    print(end - start)

