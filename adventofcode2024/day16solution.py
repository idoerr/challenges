
class MinHeap:
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def add(self, element):
        self.queue.append(element)

        self._sift_up(len(self.queue) - 1)

    def pop(self):
        min_element = self.queue[0]
        last_element = self.queue.pop()

        if len(self.queue) > 0:
            self.queue[0] = last_element

            self._sift_down(0)

        return min_element

    def _sift_down(self, index):
        _children_indexes = self._children_indexes(index)
        if _children_indexes is None:
            return

        for child_index in sorted(_children_indexes, key=lambda x: self.queue[x]):
            if self.queue[index] > self.queue[child_index]:
                temp = self.queue[index]
                self.queue[index] = self.queue[child_index]
                self.queue[child_index] = temp
                self._sift_down(child_index)


    def _sift_up(self, index):
        if index == 0:
            return
        
        parent_index = self._parent_index(index)
        if self.queue[index] < self.queue[parent_index]:
            temp = self.queue[index]
            self.queue[index] = self.queue[parent_index]
            self.queue[parent_index] = temp

            self._sift_up(parent_index)
        
    
    def _parent_index(self, n):
        return (n - 1) // 2
    
    def _children_indexes(self, n):
        if len(self) <= n * 2:
            return None
        return filter(lambda x: x < len(self), ((n * 2) + 1, n * 2 + 2))

    def __str__(self):
        return str(self.queue)

turn_left_map = {
    (1, 0): (0, -1),
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (0, -1): (-1, 0)
}

turn_right_map = {
    (1, 0): (0, 1),
    (-1, 0): (0, -1),
    (0, 1): (-1, 0),
    (0, -1): (1, 0)
}

def add_points(a, b):
    return a[0] + b[0], a[1] + b[1]

def add_point_to_path(path, point, direction):
    path_copy = set(path)
    path_copy.add((point, direction))
    return path_copy

def merge_path(path_a, path_b):
    return path_a.union(path_b)

def can_travel_to_point(maze, point, direction):
    return not maze[point[0]][point[1]] == '#'
    
def add_point_to_search_queue(maze, search_queue, visited_point_costs, position, direction, path, cost): 
    new_position = add_points(position, direction)
    if can_travel_to_point(maze, new_position, direction):
        new_path = add_point_to_path(path, new_position, direction)
        search_queue.add((cost, new_position, direction, new_path))

def find_path_in_maze_using_dijkstra(maze, start_pos, start_dir, end_pos):

    visited_point_costs = {}

    min_path = None
    min_cost = None
    min_visited_tiles = set()

    search_queue = MinHeap()
    search_queue.add((0, start_pos, start_dir, set()))

    cur_cost = 0

    while len(search_queue) > 0:
        cur_cost, cur_pos, cur_direction, cur_path = search_queue.pop()

        # Once we have a valid path, don't explore paths longer than this.
        if min_cost is not None and cur_cost > min_cost:
            continue
        elif cur_pos == end_pos:
            if min_cost is None or cur_cost < min_cost:
                min_cost = cur_cost
                min_path = cur_path
                min_visited_tiles = set(cur_path)
            else:
                min_visited_tiles = min_visited_tiles.union(cur_path)
        else:
            visit_key = (cur_pos, cur_direction)
            if visit_key not in visited_point_costs:
                visited_point_costs[visit_key] = cur_cost, cur_path
            else:
                visited_cost, visited_path = visited_point_costs[visit_key]

                # Keep track of all paths that lead to this point
                if visited_cost == cur_cost:                    
                    new_visited_path = merge_path(visited_path, cur_path)
                    visited_point_costs[visit_key] = (visited_cost, new_visited_path)
                    continue
                elif visited_cost < cur_cost:
                    continue

            turn_cost = cur_cost + 1001

            # Handle turning left
            left_direction = turn_left_map[cur_direction]
            add_point_to_search_queue(maze, search_queue, visited_point_costs, cur_pos, left_direction, cur_path, turn_cost)

            # Handle turning right
            right_direction = turn_right_map[cur_direction]
            add_point_to_search_queue(maze, search_queue, visited_point_costs, cur_pos, right_direction, cur_path, turn_cost)
            
            # Handle going straight.  Note that straight first is always the cheapest option
            straight_cost = cur_cost + 1
            add_point_to_search_queue(maze, search_queue, visited_point_costs, cur_pos, cur_direction, cur_path, straight_cost)
    
    return min_path, min_cost, min_visited_tiles, visited_point_costs
            
            

if __name__ == '__main__':
    file_name = 'adventofcode2024/day16input.txt'

    maze = []

    found_blank_line = False

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            line = line.strip()

            maze.append(line)

    start_loc = None
    start_direction = (0, 1)
    end_loc = None

    for i_row, row in enumerate(maze):
        for i_col, val in enumerate(row):
            if val == 'S':
                start_loc = (i_row, i_col)
            elif val == 'E':
                end_loc = (i_row, i_col)

    found_path, found_cost, found_min_path_points, visited_point_costs = find_path_in_maze_using_dijkstra(maze, start_loc, start_direction, end_loc)

    output_map = []

    # We kept track of sub-paths to points in visited_point_costs
    # Secondary paths are not propagated up the chain though
    # We need to check each step in the path, to see if it has sub-paths.
    # If it does, add the points of the sub-path to the points list
    # Sub-paths can have their own sub-paths.  So we need to check the new points for sub-paths
    def all_paths_points():
        final_points = set(found_min_path_points)
        search_points = set(found_min_path_points)

        while len(search_points) != 0:
            next_search_points = set()

            for point in search_points:
                if point not in visited_point_costs:
                    continue
                min_path_to_point = visited_point_costs[point][1]
                next_search_points = next_search_points.union(min_path_to_point)
            
            next_search_points = next_search_points.difference(final_points)
            final_points = final_points.union(search_points)
            search_points = next_search_points

        # points have both coordinates and directions.  Discard the directions
        return set(x[0] for x in final_points)

    all_visited_paths_points = all_paths_points()

    for i_row, row in enumerate(maze):
        row_str = ''
        for i_col, val in enumerate(row):
            if (i_row, i_col) in all_visited_paths_points:
                row_str += 'x'
            else:
                row_str += val
        print(row_str)

    print()
    print(found_cost)
    print(1 + len(all_visited_paths_points))
    