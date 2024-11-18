

if __name__ == "__main__":
    file_name = 'adventofcode2023/day4puz1input.txt'

    card_scores = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            card_str, number_str = line.split(':', 1)

            winning_num_str, have_num_str = number_str.split('|', 1)

            winning_split = winning_num_str.split(' ')
            winning_set = set()
            for x in winning_split:
                if x == '':
                    continue
                winning_set.add(int(x))

            match_count = 0

            for num_str in have_num_str.split(' '):
                if num_str == '':
                    continue
                number = int(num_str)
                if number in winning_set:
                    match_count += 1
            
            card_score = 2 ** (match_count-1) if match_count > 0 else 0

            card_scores.append(card_score)

    print('complete!')
    print(sum(card_scores))