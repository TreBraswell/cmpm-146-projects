
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
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

    current = node
    ucb = {}

    while current.visits != 0:
        for child in current.child_nodes:
            ucb[child] = child.wins/child.visits + 2 * (math.sqrt((2 * math.log(child.parent.visits))/ child.visits))
            index ++
        key_list = list(ucb.keys())
        val_list = list(ucb.values())
        current = key_list[val_list.index(max(ucb))]

    leaf_node = current
    # leaf_node = node.untried_actions[random.randrange(0, len(node.untried_actions))]

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
    actions = parent_node.untried_actions

    child_node = MCTSNode(parent=parent_node, parent_action=parent_node.untried_actions[0], action_list=parent_node.untried_actions)

    parent_node.child_nodes.append(child_node)

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
    pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    # Update node.wins and node.visit
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node



        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return None
