
from bisect import bisect

class IdMapper:

    def __init__(self, file_handle):
        self._maps = {}

        next_line = None
        while file_handle.readable():
            next_line = file_handle.readline()
            if next_line.strip() == '':
                break
            self.add_mapping(next_line)

        self._rangestarts = list(sorted(self._maps.keys()))

    def add_mapping(self, str_map):
        dest_start_index, src_start_index, count = map(int, str_map.split(' ', 2))

        src_end_index = src_start_index + count - 1

        self._maps[src_start_index] = (src_start_index, src_end_index, dest_start_index)

    def get_mapping(self, id_no):
        mapping_index = bisect(self._rangestarts, id_no) - 1
        if mapping_index == -1:
            return id_no
        
        map_info = self._maps[self._rangestarts[mapping_index]]
        src_start_index, src_end_index, dest_start_index = map_info
        
        if id_no >= src_start_index and id_no <= src_end_index:
            return dest_start_index + id_no - src_start_index
        else:
            return id_no

    

    def __str__(self):
        return str(self._maps)

if __name__ == "__main__":
    file_name = '2023/day5puz1input.txt'

    with open(file_name, 'r') as file_handle:

        seed_line = file_handle.readline()
        seed_list = list(map(int,(seed_line.split(': ')[1]).split(' ')))
        print(seed_list)

        file_handle.readline()

        seed_soil_map_header = file_handle.readline()
        seed_soil_map = IdMapper(file_handle)

        soil_fertilizer_header = file_handle.readline()
        soil_fertilizer_map = IdMapper(file_handle)

        fertilizer_water_header = file_handle.readline()
        fertilizer_water_map = IdMapper(file_handle)

        water_light_header = file_handle.readline()
        water_light_map = IdMapper(file_handle)

        light_temperature_header = file_handle.readline()
        light_temperature_map = IdMapper(file_handle)

        temperature_humidity_header = file_handle.readline()
        temperature_humidity_map = IdMapper(file_handle)

        humidity_location_header = file_handle.readline()
        humidity_location_map = IdMapper(file_handle)

    min_location = -1

    for seed in seed_list:
        soil = seed_soil_map.get_mapping(seed)
        fertilizer = soil_fertilizer_map.get_mapping(soil)
        water = fertilizer_water_map.get_mapping(fertilizer)
        light = water_light_map.get_mapping(water)
        temperature = light_temperature_map.get_mapping(light)
        humidity = temperature_humidity_map.get_mapping(temperature)
        location = humidity_location_map.get_mapping(humidity)
        print(seed, soil, fertilizer, water, light, temperature, humidity, location)

        if min_location == -1:
            min_location = location
        else:
            min_location = min(location, min_location)
    
    print(min_location)


