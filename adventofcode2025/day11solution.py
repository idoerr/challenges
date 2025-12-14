from collections import defaultdict, deque

def gen_topological_sort(vertex_edge_dict):
    # Using Kahn's algorithm

    vertex_list = vertex_edge_dict.keys()
    vertex_indegree_count = defaultdict(int)

    # Count how many incoming edges lead to a vertex (called indegree)
    for vertex, edge_list in vertex_edge_dict.items():
        for end_vertex in edge_list:
            vertex_indegree_count[end_vertex] += 1
    
    visit_queue = deque()

    # find nodes with indegree = 0, place them in the queue
    # since we are using a default dict, this is equivalent to the vertex not being in the dict.
    for vertex in vertex_list:
        if vertex not in vertex_indegree_count:
            visit_queue.append(vertex)

    output_list = []

    # While the queue isn't empty, add vertexes to the output list
    while len(visit_queue) > 0:
        vertex = visit_queue.popleft()
        output_list.append(vertex)

        # Now 'remove' the vertex from the graph
        # We do this by undoing the indegree counting from before
        # For each edge this vertex leads to, decrement the indegree count by one
        # Then, if the updated indegree count == 0, add it to the queue.
        edge_list = vertex_edge_dict[vertex]

        for end_vertex in edge_list:
            vertex_indegree_count[end_vertex] -= 1

            if vertex_indegree_count[end_vertex] == 0:
                visit_queue.append(end_vertex)
    
    return output_list

def count_ways_between_nodes(vertex_edge_dict, source, dest):
    topological_visit_list = gen_topological_sort(vertex_edge_dict)

    number_ways_to_vertex_dict = defaultdict(int)
    number_ways_to_vertex_dict[source] = 1

    for vertex in topological_visit_list:
        ways_to_this_vertex = number_ways_to_vertex_dict[vertex]
        for end_vertex in vertex_edge_dict[vertex]:
            number_ways_to_vertex_dict[end_vertex] += ways_to_this_vertex
    
    return number_ways_to_vertex_dict[dest]


if __name__ == '__main__':
    file_name = 'adventofcode2025/day11input.txt'

    vertex_edge_dict = {'out': []}

    with open(file_name, 'r') as file_handle:
        for line in file_handle:
            source_node, dest_node_list_str = line.split(':')
            source_node = source_node.strip()

            dest_node_list = dest_node_list_str.strip().split()
            vertex_edge_dict[source_node] = dest_node_list

    print(count_ways_between_nodes(vertex_edge_dict, 'you', 'out'))

    svr_to_fft_ways = count_ways_between_nodes(vertex_edge_dict, 'svr', 'fft')
    fft_to_dac_ways = count_ways_between_nodes(vertex_edge_dict, 'fft', 'dac')
    dac_to_out_ways = count_ways_between_nodes(vertex_edge_dict, 'dac', 'out')

    print(svr_to_fft_ways, fft_to_dac_ways, dac_to_out_ways)

    ways_via_fft_dac = svr_to_fft_ways * fft_to_dac_ways * dac_to_out_ways

    svr_to_dac_ways = count_ways_between_nodes(vertex_edge_dict, 'svr', 'dac')
    dac_to_fft_ways = count_ways_between_nodes(vertex_edge_dict, 'dac', 'fft')
    fft_to_out_ways = count_ways_between_nodes(vertex_edge_dict, 'fft', 'out')

    ways_via_dac_fft = svr_to_dac_ways * dac_to_fft_ways * fft_to_out_ways

    print(svr_to_dac_ways, dac_to_fft_ways, fft_to_out_ways)

    print(ways_via_fft_dac + ways_via_dac_fft)
    



    
