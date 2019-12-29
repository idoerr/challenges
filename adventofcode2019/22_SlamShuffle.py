
import numpy as np

def cut_deck(deck, cut_index):
    return np.concatenate([deck[cut_index:], deck[0:cut_index]])

def deal_into_new_stack(deck):
    return np.flip(deck)

def deal_with_increment(deck, increment_val):
    new_arr = np.empty(len(deck), dtype="i")
    
    for i, cp_ind in enumerate(range(0, len(deck) * increment_val, increment_val)):
        new_arr[cp_ind % len(deck)] = deck[i]
    
    return new_arr

input_file = 'adventofcode2019/22_SlamShuffle.txt'

if __name__ == "__main__":

    file_obj = open(input_file, 'r')

    deck_len = 10007
    deck = np.array(range(deck_len))

    for line in file_obj.readlines():
        line = line.strip()
        words = line.split()

        if words[0] == "cut":
            cut_index = int(words[1])
            deck = cut_deck(deck, cut_index)
        elif words[0] == "deal":

            if words[1] == "with":
                increment_val = int(words[3])
                deck = deal_with_increment(deck, increment_val)
            else:
                # This should be "Deal into new stack"
                deck = deal_into_new_stack(deck)

    print(np.where(deck == 2019))
