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
				print("found source box: ", key, "\n")
				print("x1: ", x1, "\n")
				print("y1: ", y1, "\n")
				print("x2: ", x2, "\n")
				print("y2: ", y2, "\n")
				#result.append(key)

		#dest box
		if dx >= x1 and dx < x2:
			if dy >= y1 and dy < y2:
				print("found destination box: ", key, "\n" )
				print("x1: ", x1, "\n")
				print("y1: ", y1, "\n")
				print("x2: ", x2, "\n")
				print("y2: ", y2, "\n")
				#result.append(key)

	#print("found boxes: ", result)
	 
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


	# path = []
	#boxes = {}

	#return path, boxes.keys()
