
from collections import defaultdict
from enum import IntEnum

card_str = '23456789TJQKA'

class HandRank(IntEnum):
    FIVE_OF_KIND = 7
    FOUR_OF_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_KIND = 4
    TWO_PAIR = 3
    PAIR = 2
    HIGH_CARD = 1

def convert_hand_arr(hand_str):
    ret_arr = []
    for x in hand_str:
        ret_arr.append(card_str.index(x))
    return ret_arr

def determine_hand(hand_arr) -> HandRank:
    freq_dict = defaultdict(int)

    for x in hand_arr:
        freq_dict[x] += 1
    
    max_freq = max(freq_dict.values())

    if max_freq == 5:
        return HandRank.FIVE_OF_KIND
    elif max_freq == 4:
        return HandRank.FOUR_OF_KIND
    elif max_freq == 3:
        if len(freq_dict.keys()) == 2:
            return HandRank.FULL_HOUSE
        else:
            return HandRank.THREE_OF_KIND
    elif max_freq == 2:
        if len(list(x for x in freq_dict.values() if x == 2)) == 2:
            return HandRank.TWO_PAIR
        else:
            return HandRank.PAIR
    else:
        return HandRank.HIGH_CARD

if __name__ == "__main__":
    file_name = '2023/day7puz1input.txt'

    hand_list = [];

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            hand_str, bid = line.split(' ', 1)

            hand_arr = convert_hand_arr(hand_str)
            bid = int(bid)

            hand_rank = determine_hand(hand_arr)

            hand_list.append((hand_rank, hand_arr, hand_str, bid))

    hand_sorted = sorted(hand_list)

    total_winnings = 0

    for i, hand in enumerate(hand_sorted):
        winnings = hand[3] * (i+1)
        print(hand[2], winnings)
        total_winnings += winnings

    print(total_winnings)


            

    
