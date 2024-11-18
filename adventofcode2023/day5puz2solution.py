
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

        # Fill in the gaps between ranges
        rangestarts = list(sorted(self._maps.keys()))

        for i in range(0, len(rangestarts) - 1):
            cur_rangestart_id = rangestarts[i]
            src_start_id, src_end_id, dest_start_id, dest_end_id = self._maps[cur_rangestart_id]

            # Create a new filler range if there is a gap between the two ranges.
            next_rangestart_id = rangestarts[i+1]
            if src_end_id != next_rangestart_id - 1:
                new_start_id = src_end_id + 1
                new_end_id = next_rangestart_id - 1
                self._maps[new_start_id] = (new_start_id, new_end_id, new_start_id, new_end_id)

        self._rangestarts = list(sorted(self._maps.keys()))

    def add_mapping(self, str_map):
        dest_start_id, src_start_id, count = map(int, str_map.split(' ', 2))

        src_end_id = src_start_id + count - 1
        dest_end_id = dest_start_id + count - 1

        self._maps[src_start_id] = (src_start_id, src_end_id, dest_start_id, dest_end_id)

    def get_mapping(self, id_no):
        mapping_index = bisect(self._rangestarts, id_no) - 1
        if mapping_index == -1:
            return id_no
        
        map_info = self._maps[self._rangestarts[mapping_index]]
        src_start_id, src_end_id, dest_start_id, dest_end_id = map_info
        
        if id_no >= src_start_id and id_no <= src_end_id:
            return dest_start_id + id_no - src_start_id
        else:
            return id_no
        
    def map_range(self, id_range):
        start_id, end_id = id_range

        start_mapping_index = bisect(self._rangestarts, start_id) - 1
        end_mapping_index = bisect(self._rangestarts, end_id) - 1

        # special case for if we are below the id range
        if end_mapping_index == -1:
            return [id_range]
        
        # special case for if we are above the id mapped id range
        if start_mapping_index == len(self._rangestarts):
            last_map_range = self._rangestarts[-1]
            src_start_id, src_end_id, dest_start_id, dest_end_id = self._maps[last_map_range]
            
            # check against the end of the last range, to see if we are above the map entirely.
            if src_end_id < start_id:
                return [id_range]
            
            remainder_start_id = dest_start_id + start_id - src_start_id

            #check to see if the last map block can contain the range
            if src_end_id > end_id:
                remainder_end_id = dest_start_id + end_id - src_start_id
                return [(remainder_start_id, remainder_end_id)]
            
            #Return two ranges, that contained within the last map block, and that overflowing
            remainder_end_id = dest_start_id + src_end_id - src_start_id

            return [(remainder_start_id, remainder_end_id), (remainder_end_id + 1, end_id)]
        
        result_ranges = []

        for i in range(start_mapping_index, end_mapping_index+1):

            # Before the first mapped range
            if i == -1:
                next_map_range = self._rangestarts[i+1]
                result_ranges.append((start_id, next_map_range-1))
                continue

            # For the last mapped range, do a special comparison for if the id range exceeds the mapped range.
            if i == len(self._rangestarts) - 1:
                
                last_map_range = self._rangestarts[-1]
                src_start_id, src_end_id, dest_start_id, dest_end_id = self._maps[last_map_range]
                
                # check against the end of the last range, to see if we are above the map entirely.
                if src_end_id < start_id:
                    result_ranges.append(id_range)
                    continue
                
                cur_start_id = max(start_id, src_start_id)
                remainder_start_id = dest_start_id + cur_start_id - src_start_id

                #check to see if the last map block can contain the range
                if src_end_id >= end_id:
                    remainder_end_id = dest_start_id + end_id - src_start_id
                    result_ranges.append((remainder_start_id, remainder_end_id))
                    continue
                
                #Return two ranges, that contained within the last map block, and that overflowing
                remainder_end_id = dest_start_id + src_end_id - src_start_id

                result_ranges.append((remainder_start_id, remainder_end_id))
                result_ranges.append((src_end_id + 1, end_id))
                continue

            # Because there are no gaps in the mappings, we can assume the start index is inside this mapping
            cur_map_range = self._rangestarts[i]
            src_start_id, src_end_id, dest_start_id, dest_end_id = self._maps[cur_map_range]

            cur_start_id = max(start_id, src_start_id)
            cur_end_id = min(end_id, src_end_id)

            cur_dest_start_id = dest_start_id + cur_start_id - src_start_id
            cur_dest_end_id = dest_start_id + cur_end_id - src_start_id

            result_ranges.append((cur_dest_start_id, cur_dest_end_id))
        
        return result_ranges


    def __str__(self):
        return str(self._maps)

if __name__ == "__main__":
    file_name = 'adventofcode2023/day5puz2input.txt'

    with open(file_name, 'r') as file_handle:

        seed_line = file_handle.readline()
        seed_number_line = list(map(int,(seed_line.split(': ')[1]).split(' ')))
        seed_id_ranges = []
        
        for i in range(0, len(seed_number_line), 2):
            seed_start = seed_number_line[i]
            seed_count = seed_number_line[i+1]

            seed_end = seed_start + seed_count - 1

            seed_id_ranges.append((seed_start, seed_end))

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

    print()
    print('k')

    # Get rid of named maps here.
    map_list = [
        seed_soil_map,
        soil_fertilizer_map,
        fertilizer_water_map,
        water_light_map,
        light_temperature_map,
        temperature_humidity_map,
        humidity_location_map
    ]

    result_id_ranges = [seed_id_ranges]

    current_id_ranges = seed_id_ranges

    # Do the range mappings for each range.
    for i, id_map in enumerate(map_list):
        
        new_id_ranges = []

        for id_range in current_id_ranges:
            new_id_ranges.extend(id_map.map_range(id_range))

        current_id_ranges = new_id_ranges
        result_id_ranges.append(current_id_ranges)

        if i == 6:
            break

    print(min(current_id_ranges)[0])

