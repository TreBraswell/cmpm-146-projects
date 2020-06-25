from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

def heuristic(a, b):
   # Manhattan distance on a square grid
   return abs(a.x - b.x) + abs(a.y - b.y)
def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    """ queue = [] # Just a plain list

heappush(queue, (2, 'a')) # enqueuing some pairs

heappush(queue, (42,'b'))

heappush(queue, (1, 'c'))

p1, x1 =  # dequeuing some pairs

p2, x2 = heappop(queue)

p3, x3 = heappop(queue)

assert [x1, x2, x3] == ['c','a','b']

assert [p1, p2, p3] == [1, 2, 42]

assert queue == [] """
    frontier = [] # our queue which we interpret  as a priority queue
    heappush(frontier, (initial_position[2],initial_position ) #putting our instial position with its cost
    came_from = {} # where we have been
    cost_so_far = {} #the cost so far
    came_from[0] = 0 #just setting up the intial destination
    cost_so_far[0] = 0 #where were starting
    i = 0;
    while not frontier.empty():
        current = heappop(frontier) # gets lowest priority
        
        if current == destination: # if it equals our goal destnation
            break
        if i not equals 0:
            adj = navigation_edges()# reset which variables were going to look at
     #adj = navigation_edges(
        for next in adj: # for all elements in adjacent to it
            new_cost = next[1] + current[1] # adding our current cost to our next element
            if next not in cost_so_far or new_cost < cost_so_far[i]:
                cost_so_far[i] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    
    pass


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """
    # a* star algorithm
    """
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

while not frontier.empty():
   current = frontier.get()

   if current == goal:
      break
   
   for next in graph.neighbors(current):
      new_cost = cost_so_far[current] + graph.cost(current, next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
         cost_so_far[next] = new_cost
         priority = new_cost
         frontier.put(next, priority)
         came_from[next] = current
    """
    pass


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    edges = []
    for i in range (-1,2):
        for j in range (-1,2):
            if i == 0 and j == 0:
                """ Do Nothing """
            elif not (cell[0]+i,cell[1]+j) in level['spaces']:
                """ Do Nothing """
            else:
                edges.append(((cell[0]+i,cell[1]+j), cost_calculator(cell, (cell[0]+i,cell[1]+j), level)))
    return edges

    pass


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'example.txt', 'a','e'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_costs.csv')



def cost_calculator(cell1, cell2, level):
    tempcost = 0.5*level['spaces'][cell1] + 0.5*level['spaces'][cell2]
    if cell1[0] == cell2[0] or cell1[1] == cell2[1]:
        return tempcost
    else
        return tempcost * sqrt(2)