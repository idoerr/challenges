
def is_password_valid_part1(pwd):
    is_increasing = True
    found_double = False

    last_val = 0
    for c in pwd:
        c_val = int(c)
        if c_val < last_val:
            is_increasing = False
        if c_val == last_val:
            found_double = True
        
        last_val = c_val
    
    return is_increasing and found_double

def is_password_valid_part2(pwd):
    is_increasing = True
    found_double = False

    last_val = 0
    match_count = 0
    for c in pwd:
        c_val = int(c)
        if c_val < last_val:
            is_increasing = False
        if c_val == last_val:
            match_count += 1
        if c_val != last_val:
            if match_count == 1:
                found_double = True
            match_count = 0
        
        last_val = c_val
    
    if match_count == 1:
        found_double = True
    
    return is_increasing and found_double

if __name__ == "__main__":

    print(is_password_valid_part2("123444"))

    left_bound = 234208
    right_bound = 765869

    value_part1 = []
    value_part2 = []

    for x in range(left_bound, right_bound + 1):

        str_x = str(x)

        if is_password_valid_part1(str_x):
            value_part1.append(x)
        
        if is_password_valid_part2(str_x):
            value_part2.append(x)
    
    print( "Part 1 Result" )
    print( len(value_part1) )

    print()

    print( "Part 2 Result" )
    print( len(value_part2) )


