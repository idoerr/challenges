
import re

if __name__ == "__main__":
    file_name = 'adventofcode2023/day2puz2input.txt'

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

    print('got this far')
    
    def powerofgame(game):
        game_id, max_reveal = game

        power = 1
        for color, count in max_reveal.items():
            power *= count
        return power

    valid_gamesum = sum(powerofgame(game) for game in game_information)

    print(valid_gamesum)




