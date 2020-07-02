
from mcts_node import MCTSNode
from random import choice
import random
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.

ROLLOUTS = 10
MAX_DEPTH = 5

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
    # me = identity
    # if me == 1:
    #     turn = me
    #     opponent = 2
    # else:
    #     opponent = 1
    #     turn = opponent

    current = node
    ucb = {}

    temp = node
    max_ucb = 0

    if current.visits != 0:
        for action in current.parent.child_nodes:

            if turn == identity:
                child = current.parent.child_nodes[action]
                exploitation = child.wins/child.visits

                exploration = 2 * (sqrt((2 * log(child.visits))/ child.visits))

                ucb[child] = exploitation + exploration

                if ucb[child] > max_ucb:
                    max_ucb = ucb[child]
                    temp = child 
            else:
                child = current.parent.child_nodes[action]
                exploitation = 1 - (child.wins/child.visits)

                exploration = 2 * (sqrt((2 * log(child.visits))/ child.visits))

                ucb[child] = exploitation + exploration

                if ucb[child] < max_ucb:
                    max_ucb = ucb[child]
                    temp = child 
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
            current = temp


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
    actions = parent_node.untried_actions

    child_node = MCTSNode(parent=parent_node, parent_action=actions[0], action_list=actions)

    parent_node.child_nodes[actions[0]] = child_node

    wins = rollout(board, board.next_state(state, actions[0])) 
    # print("Wins: ", wins)
    backpropagate(child_node, wins)

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



    moves = board.legal_actions(state)
    if len(moves) == 0:
        return 0
    best_move = moves[0]
    best_expectation = float('-inf')

    me = board.current_player(state)

    def outcome(owned_boxes, game_points):
        if game_points is not None:
            # Try to normalize it up?  Not so sure about this code anyhow.
            red_score = game_points[1]*9
            blue_score = game_points[2]*9
        else:
            red_score = len([v for v in owned_boxes.values() if v == 1])
            blue_score = len([v for v in owned_boxes.values() if v == 2])
        return red_score - blue_score if me == 1 else blue_score - red_score

    for move in moves:
        total_score = 0.0

        # Sample a set number of games where the target move is immediately applied.
        for r in range(ROLLOUTS):
            rollout_state = board.next_state(state, move)

            # Only play to the specified depth.
            for i in range(MAX_DEPTH):
                if board.is_ended(rollout_state):
                    break
                rollout_move = random.choice(board.legal_actions(rollout_state))
                rollout_state = board.next_state(rollout_state, rollout_move)

            total_score += outcome(board.owned_boxes(rollout_state),
                                   board.points_values(rollout_state))

        expectation = float(total_score) / ROLLOUTS

        # If the current move has a better average score, replace best_move and best_expectation
        if expectation > best_expectation:
            best_expectation = expectation
            best_move = move

    if best_expectation > 0:
        best_expectation = 1
    elif best_expectation < 0:
        best_expectation = -1
    else:
        best_expectation = 0
    return best_expectation


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.
    
    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """

    # Update node.wins and node.visit
    if node.parent == None:
        node.visits += 1
        node.wins += won
        return node
    node.wins += won
    node.visits += 1
    # print("node wins: ", node.wins)
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


    most_wins = root_node
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        leaf_node = traverse_nodes(root_node, board, state, identity_of_bot)
        child_node = expand_leaf(leaf_node, board, state)

        # print("This is child_node.wins: ", child_node.wins)
        if child_node.wins >= 1.0 or child_node.wins <= -1.0 or child_node.wins == 0:
            # print("Returns")
            return child_node.parent_action
        root_node = child_node 


        # Do MCTS - This is all you!

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return child_node.parent_action
