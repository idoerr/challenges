
import re

if __name__ == "__main__":
    file_name = '2023/day2puz1input.txt'

    max_values = {'green': 13, 'red':12, 'blue': 13}

    game_information = []

    with open(file_name, 'r') as file_handle:
        for line in file_handle:

            game_str, game_turns = line.split(':', 1)

            game_id = int(game_str.strip().split(' ')[1])
            max_reveal = {'green': 0, 'red':0, 'blue': 0}

            show_list = re.split( '[;,] ', game_turns.strip() )
            for show_str in show_list:
                color_count, color_name = show_str.split(' ', 1)
                color_count = int(color_count)

                max_color = max_reveal[color_name]
                max_color = max(color_count, max_color)
                max_reveal[color_name] = max_color
            
            game_information.append( (game_id, max_reveal) )
    
    def check_validgame( game ):
        game_id, max_reveal = game

        for color, count in max_reveal.items():
            if count > max_values[color]:
                return False
            
        return True
    
    print('got this far')

    filtered_games = [ game_info for game_info in game_information if check_validgame(game_info) ]

    valid_gamesum = sum(game_id for game_id, max_reveal in filtered_games)

    print(valid_gamesum)




