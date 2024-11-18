

if __name__ == "__main__":
    file_name = 'adventofcode2023/day4puz2input.txt'

    card_matches = []

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
            
            card_matches.append(match_count)
    
    card_counts = [1] * len(card_matches)
    #card_counts[0] = 1
    card_index = 0

    for card_index in range(0, len(card_counts)):
        number_of_cards = card_counts[card_index]
        cur_match_count = card_matches[card_index]

        for match_offset in range(0, cur_match_count):
            new_card_index = card_index + match_offset + 1

            card_counts[new_card_index] += number_of_cards

    print('complete!')
    print(card_counts)
    print(sum(card_counts))