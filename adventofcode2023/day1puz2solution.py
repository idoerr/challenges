
if __name__ == "__main__":
    file_name = 'adventofcode2023/day1puz2input.txt'

    row_values = [];

    string_map = { 'one':1, 'two':2, 'three':3, 'four':4, 
                  'five':5, 'six':6, 'seven':7, 'eight':8,
                  'nine':9, 'zero':0, '1':1, '2':2, '3':3,
                  '4':4, '5':5, '6':6, '7': 7, '8':8, '9':9, '0':0 }

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            min_index = 999999
            min_value = 0
            max_index = -1
            max_value = 0

            for search_str in string_map.keys():
                

                first_find = line.find(search_str)
                if first_find != -1 and first_find < min_index:
                    min_index = first_find
                    min_value = string_map[search_str]
                
                last_find = line.rfind(search_str)
                if last_find != -1 and last_find > max_index:
                    max_index = last_find
                    max_value = string_map[search_str]

            value = min_value * 10 + max_value

            row_values.append(value)

    print(sum(row_values))