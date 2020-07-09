import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush
Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.
    #for loop that looks at each item then checks whether their in thier or we can use find
    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        #if we can look at requiremntes
        if 'Consumes' in rule:
            for (item, atm) in rule['Consumes'].items():
                if state[item] >= atm:
                    continue
                else:
                    return False
        if 'Requires' in rule :
            #loop for each item in our state
            for (item, bool) in rule['Requires'].items():
                if state[item]>=1:
                    continue
                else:
                    return False
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        if 'Consumes' in rule:
            for (item, atm) in rule['Consumes'].items():
                next_state[item] -= atm
        for (item, atm) in rule['Produces'].items():
            next_state[item] += atm
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for (item, atm) in goal.items():
            if state[item] < atm:
                return False
        return True

    return is_goal

def make_heuristic(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.
    def heuristic(state, recipe):
        # This code is used in the search process and may be called millions of times.
        tools = {"", "bench","wooden_pickaxe", "wooden_axe", "stone_pickaxe", "stone_axe", "furnace", "iron_pickaxe", "iron_axe"}
        cost = 0
        if is_goal(state):
            return 0
        for (item, amt) in state.items():
            if item in tools and amt>1:
                return -1
            if amt>8:
                return -1
        cur_tool = 0
        for (index, tool) in enumerate(tools, start=1):
            if state[tool] == 1:
                cur_tool = index
            else:
                break


        '''
        for (item, val) in goal_item_min_cost.items():
            diff = state[item] - val['amount']
            if diff>0:
                cost += diff * val['time']
                print("missing ", item, ",add", cost)
                for (item2, amt2) in val['Consumes']:
                    diff2 = state[item2] - amt2
                    if diff2>0:
                        cost+=diff * diff2
        '''
        return cost
    return heuristic


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            #print("graph:",r.name, r.effect(state), r.cost)
            yield (r.name, r.effect(state), r.cost)

'''
def heuristic(state):
    # Implement your heuristic here!
    return 0
'''

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()
    frontier = [] # our queue which we interpret  as a priority queue
    heappush(frontier, (0,state) ) #putting our instial position with its cost
    came_from = {} # where we have been
    cost_so_far = {} #the cost so far
    came_from[state] = 0 #just setting up the intial destination
    cost_so_far[state] = 0 #where were starting
    done = 0
    counter = 0
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while frontier:

        (cur_cost, current) = heappop(frontier) # gets lowest priority
        print("current cost", cur_cost)
        if is_goal(current): # if it equals our goal destnation
            print("final state:", current, "final cost:", cur_cost)
            destination = current
            done = 1
            break
        print("loop "+str(counter), ", cobble:", state["cobble"])
        counter+=1
        for next in graph(current): # for all elements in adjacent to it
            h = heuristic(next[1], next[0])
            if h == (-1):
                continue
            if next[1] in cost_so_far.keys():
                if next[2]+cur_cost <cost_so_far[next[1]]:
                    cost_so_far[next[1]] = next[2] +cur_cost
                    came_from[next[1]] = current
            else:
                cost_so_far[next[1]] = next[2] +cur_cost
                came_from[next[1]] = current
                priority = cost_so_far[next[1]] + h
                print("priority", priority, "cost so far", cur_cost, "recipe cost", next[2])
                print("recipe name", next[0])
                print("cobble:", next[1]["cobble"])
                heappush(frontier,(priority,next[1]))
                #print("pushed", next)

    if done == 1:

        goback = []
        current = destination
        while current != 0:
            goback.insert(0,current)
            #print("test")
            current = came_from[current]
        print("final length", len(goback))

    print(time() - start_time, 'seconds.')
    if done == 1: # if it equals our goal destnation
        print("success")
    else:
    # Failed to find a path
        print("Failed to find a path from", state, 'within time limit.')
        return None

def get_relevent_items(goal):
    init = goal.keys()
    result = []
    for r in all_recipes:
        if r['']

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])
    goal_item_min_cost = {}

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        """
        product = rule['Produces'].keys()[0]
        print("product", product)
        if product in Crafting['Goal'] and (product not in goal_item_min_cost or rule['time'] < goal_item_min_cost[product]):
            goal_item_min_cost[product] =  {"amount":Crafting['Goal'][product], "time":rule['Time'], "Consumes":rule['Consumes']}
        """
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)
    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])
    heuristic = make_heuristic(Crafting['Goal'])
    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    print("this is state : ", str(state))
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
