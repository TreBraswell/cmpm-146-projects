from heapq import heappop, heappush
from math import inf, sqrt
def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: adjacent cells to cell
        cell: A target location.

    Returns:
        A list of costs and adjacent boxes
    """


    edges = []
    # Visit all adjacent cells
    for box in level:
            
        #########
        #NOTE : i used the lower number ie the start of the box
        #########
        # calculate the distance from cell to next_cell
        dist = sqrt((box[2] - cell[2]) ** 2 + (box[0] - cell[0]) ** 2) * 0.5
        # calculate cost and add it to the dict of adjacent cells
        edges.append((dist,box))
    return edges
    pass

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
    boxes = mesh["boxes"]
    adj = mesh["adj"]
    result = []
    #key[0] = x1 key[1] = y1 key[2] = x2 key[3] = y2
    
    sx = source_point[1]
    sy = source_point[0]
    dx = destination_point[1]
    dy = destination_point[0]

    print("source_point: ", sx, ", ", sy)
    print("destination_point: ", dx, ", ", dy)

    for key in boxes:
        x1 = key[2]
        x2 = key[3]
        y1 = key[0]
        y2 = key[1]
        
        #if x2 > 900:
            #print("yes")
        #source box
        if sx >= x1 and sx < x2:
            if sy >= y1 and sy < y2:
                sourcebox = key
                print("found source box: ", key, "\n")
                print("x1: ", x1, "\n")
                print("y1: ", y1, "\n")
                print("x2: ", x2, "\n")
                print("y2: ", y2, "\n")
                #result.append(key)

        #dest box
        if dx >= x1 and dx < x2:
            if dy >= y1 and dy < y2:
                destinationbox = key
                print("found destination box: ", key, "\n" )
                print("x1: ", x1, "\n")
                print("y1: ", y1, "\n")
                print("x2: ", x2, "\n")
                print("y2: ", y2, "\n")
                #result.append(key)

    #print("found boxes: ", result)
     

    # The priority queue
    queue = []
    print(sourcebox)
    heappush(queue,(0,sourcebox))

    # The dictionary that will be returned with the costs
    distances = {}
    distances[sourcebox] = 0

    # The dictionary that will store the backpointers
    backpointers = {}
    backpointers[sourcebox] = None

    while queue:
        current_dist, current_node = heappop(queue)

        # Check if current node is the destination
        if current_node == destinationbox:

            # List containing all cells from initial_position to destination
            #path = [current_node]
            for boxf in backpointers:
                print(boxf)
            # Go backwards from destination until the source using backpointers
            # and add all the nodes in the shortest path into a list
            #current_back_node = backpointers[current_node[1]]
            #while current_back_node is not None:
             #   print(current_back_node)
              #  path.append(current_back_node)
              #  current_back_node = backpointers[current_back_node]

            return path[::-1]

        # Calculate cost from current note to all the adjacent ones
        for adj_node, adj_node_cost in navigation_edges(adj[current_node],current_node):
            print(current_dist)
            print(adj_node_cost)
            pathcost = current_dist[0] + adj_node_cost[0] # their is going to some errors because i am just adding them all together

            # If the cost is new
            ######
            #NOTE: may have to check that i am checking distances correctly
            ######
            if adj_node[1] not in distances or pathcost < distances[adj_node[1]]:
                distances[adj_node[1]] = pathcost
                backpointers[adj_node[1]] = current_node[0]
                heappush(queue, (pathcost, adj_node[1]))


    # path = []
    #boxes = {}

    #return path, boxes.keys()
