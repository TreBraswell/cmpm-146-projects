
from mcts_node import MCTSNode
from random import choice
import random
from math import sqrt, log
#how do we improve our algorithm?
#why does backpropagate not work?
#The flip(i.e how do we use the function  for the opponent)
#is rollout correct?
num_nodes = 100
explore_faction = 2.


def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.
    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.
    Returns:        A node from which the next stage of the search can proceed.
    """

    # For first node, will pick root because it is also leaf node
    # UCB - X is how many times won over how many times played (visited)
    # x = node.wins/node.visits (if visits != 0)
    # C is hardcoded, we can choose. Lower C value is exploitation, higher is exploration.
    # Try C = 2
    # Use highest UCB to choose each node down a path until leaf_node is reached
    turn = identity
    current = node
    # index = 0
    # while len(current.child_nodes) != 0:
    #     for action in current.child_nodes:
    #         current = current.child_nodes[action]
    #         print("index: ", index)
    #         print("action: ", action)
    #         index += 1
    ucb = {}

    temp = node
    max_ucb = 0

    i = 0
    updatestate = state
    # a = len(current.child_nodes)
    while len(current.child_nodes) != 0:
        for action in current.child_nodes:
            # print(i)
            i = i +1
            if current.child_nodes[action].visits == 0 :
                #print(len(current.child_nodes))
                child = current.child_nodes[action]
                exploitation = child.wins/child.visits

                exploration = 2 * (sqrt((2 * log(child.parent.visits))/ child.visits))

                ucb[child] = exploitation + exploration

                if ucb[child] > max_ucb:
                    max_ucb = ucb[child]
                    temp = child 
           
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
            current = current.child_nodes[action]
            updatestate = board.next_state(updatestate, action)


    leaf_node = current

    return leaf_node
    # Hint: return leaf_node



def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.
    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.
    Returns:    The added child node.
    """

    # Create new node from parent node
    # Can choose action randomly
    # Action list comes from node.untried_actions?
    parent_node = node 
    actions1 = board.legal_actions(state)
    state2 = board.next_state(state, actions1[0])
    actions2 = board.legal_actions(state2)
    #print(actions[0])
    # print("this is the length before ",len(parent_node.child_nodes) )
    child_node = MCTSNode(parent=parent_node, parent_action=actions1[0], action_list=board.legal_actions(state2))
    try:
        parent_node.child_nodes[actions2[0]] = child_node
    except: 
        return child_node
        parent_node.child_nodes[actions1[0]] = child_node
        print("it broke", actions2, "also :", actions1)
    # print("this is the length after",len(parent_node.child_nodes) )
    return child_node

    
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.
    Args:
        board:  The game setup.
        state:  The state of the game.
    return state/ board at the end - see who won
    """

    # Return who won this game (board or state)
    # board.is_ended(state) == true when over
    # Same as Rollout bot, can basically copy/paste
    # pass

    while not  board.is_ended(state):
        move = random.choice(board.legal_actions(state))
        state = board.next_state(state,move)

    return board.current_player(state)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.
    """
    if node.parent == None:
        node.visits += 1
        node.wins += won
        return node
    node.wins += won
    node.visits += 1

    return backpropagate(node.parent, won)


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.
    Args:
        board:  The game setup.
        state:  The state of the game.
    Returns:    The action to be taken.
    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    i = 0

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        #print("this is the length : ",len(root_node.child_nodes))

        leaf_node = traverse_nodes(root_node, board, sampled_game, identity_of_bot)
        child_node = expand_leaf(leaf_node, board, state)
        if len(child_node.untried_actions) == 0:
            print("drawsss")
            bestAction = child_node.parent_action
            break
        parent_node = child_node.parent
        actions = parent_node.untried_actions
        wins = rollout(board, board.next_state(state, actions[0])) 

        temp = child_node
        temp.visits += 1
        temp.wins += wins
        while temp.parent !=None:
            temp = temp.parent
            temp.visits += 1
            temp.wins += wins
        
        root_node = temp
    
        high=-1
    #print("test2")
    for node in root_node.child_nodes:
        temp2=root_node.child_nodes[x]
        if ((temp2.wins/temp2.visits)>high) and node!=None:
            score=(temp2.wins/temp2.visits)
            best=node

    return best