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
        """
      frontier = [] # our queue which we interpret  as a priority queue
    heappush(frontier, (heuristic(initial_position,destination),initial_position) ) #putting our instial position with its cost
    came_from = {} # where we have been
    cost_so_far = {} #the cost so far
    came_from[initial_position] = 0 #just setting up the intial destination
    cost_so_far[initial_position] = 0 #where were starting
    done = 0
    while frontier:
        current = heappop(frontier) # gets lowest priority
        if current[1] == destination: # if it equals our goal destnation
            done = 1
            break
        adjacents = adj(graph,current[1])# reset which variables were going to look at
     #adj = navigation_edges(

        for next in adjacents: # for all elements in adjacent to it
            if next[0] in cost_so_far.keys():
                if (next[1]+cost_so_far[current[1]]) <cost_so_far[next[0]]:
                    cost_so_far[next[0]] = next[1] +cost_so_far[current[1]]
                    came_from[next[0]] = current[1]
            else:
                cost_so_far[next[0]] =  next[1] +cost_so_far[current[1]]
                came_from[next[0]] = current[1]
                priority = cost_so_far[next[0]] + heuristic(next[0],destination)
                heappush(frontier,(priority,next[0]))
    if done == 1:

        goback = []
        current = destination
        while current != 0:
            goback.insert(0,current)

            current = came_from[current]
        return goback
    return None     
    pass    """

    frontier = [(initial_position, 0)]
    previous = {}
    move_cost = {}
    previous[initial_position] = None
    move_cost[initial_position] = 0

    while frontier:
        current_pos, current_cost = heappop(frontier)

        if current_pos == destination:
            path = []
            current_path = destination
            while current_path != None:
                path.insert(0, current_path)
                current_path = previous[current_path]
            return path

        for next_node, next_cost in adj(graph, current_pos):
            new_cost = move_cost[current_pos] + next_cost
            if next_node not in move_cost or new_cost < move_cost[next_node]:
                move_cost[next_node] = new_cost
                temp_cost = new_cost
                heappush(frontier, (next_node, temp_cost))
                previous[next_node] = current_pos

    return None


    path = []
    boxes = {}

    return path, boxes.keys()
