import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush
from math import ceil
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

def make_heuristic(goal, recipes, goal_item_min_cost):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.
    '''
    materials = ["planck","cobble", "ingot"]
    materail_to_tool = {"planck":["bench","wooden_axe"], "cobble":["wooden_pickaxe","stone_pickaxe"], "ingot": ["iron_pickaxe", "furnace"]}
    for product in goal_item_min_cost['Consumes']:
        if product in materials
    '''
    products = set(goal.keys())
    observed = set()
    required_tools = set()
    required_materials= set()
    while products:
        components = set()
        for r in recipes.values():
            product = next(iter(rule['Produces'].keys()))
            if product not in observed and product in products:
                if "Consumes" in r:
                    components.update(r['Consumes'].keys())
                if "Requires" in r:
                    required_tools.update(r['Requires'].keys())
                    components.update(r['Requires'].keys())
        observed.update(products)
        products = components
    limits = { "bench":1,
               "cart":0,
               "coal":1,
               "cobble":8,
               "furnace":1,
               "ingot":8,
               "iron_axe":0,
               "iron_pickaxe":1,
               "ore":1,
               "plank":8,
               "rail":0,
               "stick":4,
               "stone_axe":1,
               "stone_pickaxe":1,
               "wood":1,
               "wooden_axe":1,
               "wooden_pickaxe":1
              }
    for item in limits:
        if item in goal and goal[item]>limits[item]:
            limits[item] = goal[item]
    axes = ["wooden_axe", "stone_axe", "iron_axe"]
    pickaxes = ["wooden_pickaxe", "stone_pickaxe", "iron_pickaxe"]

    def heuristic(state, recipe_name):
        # This code is used in the search process and may be called millions of times.
        #crafttools = ["craft bench","craft wooden_pickaxe at bench","craft wooden_axe at bench","craft stone_pickaxe at bench","craft stone_axe at bench","craft furnace at bench","craft iron_pickaxe at bench"]
        cost = 0
        new_item = next(iter(recipes[recipe_name]['Produces'].keys()))
        #print("new_item",new_item)
        new_amt = next(iter(recipes[recipe_name]['Produces'].values()))
        '''
        if new_item == "iron_axe":
            return -1
        if (new_item in tools or new_item in fast_moving_goods) and state[new_item] >1:
            return -1
        limit = max(goal[new_item], 8) if new_item in goal else 8
        print("limit", max(goal['rail'], 8))
        if state[new_item] > limit:
            return -1
        '''
        if is_goal(state):
            return 0
        if state[new_item] > limits[new_item]:
            return -1
        #if state["furnace"]>=1 and 

        if recipe_name == "punch for wood" and (state['stone_axe'] >=1 or state['iron_axe'] >=1 or  state['wooden_axe'] >=1 ):
            return -1
        if 'Requires' in recipes[recipe_name]:
            tool = next(iter(recipes[recipe_name]['Requires'].keys()))
            if tool == "wooden_axe" and (state['stone_axe'] >=1 or state['iron_axe'] >=1):

                return -1
            if tool == "stone_axe" and state['iron_axe'] >=1:
                return -1
            if tool == "wooden_pickaxe" and (state['stone_pickaxe'] >=1 or state['iron_pickaxe'] >=1):
                return -1
            if tool == "stone_pickaxe" and state['iron_pickaxe'] >=1:
                return -1

        for tool in required_tools:
            if state[tool] == 0:
                cost+=1


        '''
        if new_item not in required_materails and new_item not in required_tools:
            print("discouraging",new_item )
            cost += 1
            else:
                cur_tool +=1
        var2 = recipes[crafttools[tools.index(required_tools[cur_tool])]]
        if new_item not in var2['Consumes']:
            print("discouraging",new_item )
            cost += 1
        '''
        for (item, val) in goal_item_min_cost.items():
            diff = val['required_amt']- state[item]
            if diff>0:
                diff = ceil(float(diff)/val['produced_amt'])
                cost += diff * val['time']
                """if 'Consumes' in val:
                    for (item2, amt2) in val['Consumes'].items():
                        diff2 = state[item2] - amt2
                        if diff2>0:
                            cost+=diff * diff2
                if 'Requires' in val:
                    for (item2, _) in val['Requires'].items():
                        if state[item2] == 0:
                            cost+=1"""
        return cost
    return heuristic


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    list = []
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def search(graph, state, is_goal, limit, heuristic):

    start_time = time()
    frontier = [] # our queue which we interpret  as a priority queue
    heappush(frontier, (0,state) ) #putting our instial position with its cost
    came_from = {} # where we have been
    cost_so_far = {} #the cost so far
    came_from[state] = (0,0) #just setting up the intial destination
    cost_so_far[state] = 0 #where were starting
    done = 0
    counter = 0
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while frontier:

        (_, current) = heappop(frontier) # gets lowest priority
        cur_cost = cost_so_far[current]
        #print("current cost", cur_cost)
        if is_goal(current): # if it equals our goal destnation
            done = 1
            goback = []
            current = (current,0)
            while current[0] != 0:
                goback.insert(0,current)
                current = came_from[current[0]]
            goback.pop()
            print(goback)
            print("final length:", len(goback))
            print("final cost:", cur_cost)
            break
        #print("loop "+str(counter))
        counter+=1
        for next in graph(current): # for all elements in adjacent to it
            h = heuristic(next[1], next[0])
            if h == -1:
                continue
            if next[1] in cost_so_far:
                if next[2]+cur_cost <cost_so_far[next[1]]:
                    cost_so_far[next[1]] = next[2] +cur_cost
                    came_from[next[1]] = (current,next[0])
            else:
                cost_so_far[next[1]] = next[2] +cur_cost
                came_from[next[1]] = (current,next[0])
                priority = cost_so_far[next[1]] + h
                #print("priority", priority, "cost so far", cur_cost, "recipe cost", next[2])
                #print("recipe name", next[0])
                heappush(frontier,(priority,next[1]))
                #print("pushed", next)


    print(time() - start_time, 'seconds.')
    if done == 1: # if it equals our goal destnation
        print("success")
    else:
    # Failed to find a path
        print("Failed to find a path from", state, 'within time limit.')
        return None

def get_relevent_tools(goal_items, recipes):
    products = set(goal_items)
    components = set()
    tools = set()
    while9


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
        product = next(iter(rule['Produces'].keys()))
        amt = next(iter(rule['Produces'].values()))
        if product in Crafting['Goal'] and (product not in goal_item_min_cost or rule['time'] < goal_item_min_cost[product]):
            goal_item_min_cost[product] =  {"produced_amt":amt, "required_amt":Crafting['Goal'][product], "time":rule['Time']}
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)
    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])
    heuristic = make_heuristic(Crafting['Goal'], Crafting['Recipes'], goal_item_min_cost)
    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
