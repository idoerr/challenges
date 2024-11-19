
def hash_str(to_hash):
    cur_hash = 0
    for x in to_hash:
        cur_hash = ((cur_hash + ord(x)) * 17) % 256
    return cur_hash

if __name__ == "__main__":
    file_name = 'adventofcode2023/day15puz1input.txt'

    str_hashes = [];

    with open(file_name, 'r') as file_handle:
        data = file_handle.read()
        
        split_str = data.split(',')
        for x in split_str:
            str_hashes.append(hash_str(x))
    print('k')
    print(sum(str_hashes))
