from heapq import heappop, heappush

def heuristic(a, b):

    return abs(int(a[0]) - int(b[0])) + abs(int(a[1]) - int(b[1]))

def find_path (source_point, destination_point, mesh):

    """
    Searches for a path from source_point to destination_point through the mesh

    Args:
        source_point: starting point of the pathfinder
        destination_point: the ultimate goal the pathfinder must reach
        mesh: pathway constraints the path adheres to

    Returns:

        A path (list of points) from source_point to destination_point if exists
        A list of boxes explored by the algorithm
    """
    
    frontier = [(source_point, 0)]
    visited = []
    previous = {}
    distance = {}
    previous[source_point] = None
    distance[source_point] = 0

    print("source point: ", source_point)
    print("dest point: ", destination_point)

    while frontier:
        current_box = heappop(frontier)

        if current_box == destination_point:
            path = []
            current_path = destination_point
            while current_path != None:
                path.insert(0, current_path)
                current_path = previous[current_path]
            return path

        visited.append(current_box)

        for adjacent_box in mesh['adj'][current_box]:
            if adjacent_box in visited:
                continue
            else:

                move_cost[next_node] = new_cost
                temp_cost = new_cost
                heappush(frontier, (next_node, temp_cost))
                previous[next_node] = current_pos"""


    path = []
    boxes = {}

    return path, boxes.keys()
