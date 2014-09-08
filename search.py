
__author__ = "Josh Kelle"

"""
Several graph search functions:
    - A* (several heuristics to choose from)
    - depth limited search
    - iterative deepening search
"""

from gamestate import Gamestate, correct_locations
from priority_queue import PriorityQueue
import time


##############
# heuristics #
##############

def dist((a,b), (x,y)):
    """
    manhattan distance
    """
    return abs(a-x) + abs(b-y)


def heuristic_0(gamestate):
    """
    null heuristic
    """
    return 0


def heuristic_1(gamestate):
    """
    Add 1 for each tile which is out of place.
    """
    global correct_locations
    grid = gamestate.grid
    cost = 0

    for row in range(4):
        for col in range(4):
            if (row, col) != correct_locations[grid[row][col]]:
                cost += 1

    return cost


def heuristic_2(gamestate):
    """
    For each tile, add manhattan distance from tile's current location
    to it's goal location.
    """
    global correct_locations
    grid = gamestate.grid
    cost = 0

    for row in range(4):
        for col in range(4):
            cost += dist((row, col), correct_locations[grid[row][col]])

    return cost


def heuristic_3(gamestate, targets):
    """
    Same as heuristic_2, but only consider certain tiles.

    parameters:
    targets -- list of integers. These are the tiles which count towards
               the heuristic value.
    """
    global correct_locations
    grid = gamestate.grid
    cost = 0

    for row in range(4):
        for col in range(4):
            if grid[row][col] in targets:
                cost += dist((row, col), correct_locations[grid[row][col]])

    return cost


######
# A* #
######

def astar(start_gamestate,
          heuristic=heuristic_3,
          targets=range(1,17),
          q=False):
    """
    parameters:
    start_gamestate -- a Gamestate object
    heuristic -- a function
    targets -- a list of (row, col) positions which need to be in the correct
               spot on the board. Determines goal state.
    q -- quiet flag. If False, print out info to give some indication of
         progress
    """
    start_time = time.time()
    cur_state = start_gamestate
    cur_actions = []
    prev_len = -1

    fringe = PriorityQueue()
    visited_states = set()

    while not cur_state.is_goal_state(targets):
        
        # print info to the screen
        # pretty poor way to track program's progress
        if not q and len(cur_actions) > prev_len:
            print len(cur_actions), time.time() - start_time
            prev_len = len(cur_actions)
        
        # remember state as visited
        visited_states.add(cur_state)

        # push neighboring states onto fringe
        for action in cur_state.get_legal_actions():
            successor = cur_state.get_successor(action)
            
            if successor not in visited_states:
                # add neighbor to fringe
                # g = len(cur_actions) + 1
                # h = heuristic
                priority = len(cur_actions) + 1 + heuristic(cur_state, targets)
                fringe.push( (successor, cur_actions + [action]), priority )

        # get next state from fringe, skipping ones we've seen already
        next_state, actions_to_next_state = fringe.pop()
        while next_state in visited_states:
            next_state, actions_to_next_state = fringe.pop()

        cur_actions = actions_to_next_state
        cur_state = next_state

    return cur_actions, cur_state


########################
# depth limited search #
########################

def iterative_deepening_dfs(start_state):
    """
    Iterative deepening depth first search.

    Return a list of actions. Actions are (row, col) tuples.
    """
    depth_limit = 0
    is_solved = False
    
    while not is_solved:
        depth_limit += 1
        print "depth_limit =", depth_limit
        is_solved, actions_to_solution = dls_helper(start_state, [], 0, depth_limit)

    assert is_solved
    return actions_to_solution


def dls(start_state, max_depth):
    """
    Depth limited search.
    
    Do dfs treating nodes at max_depth as leaves.
    Don't stop on first solution; remember all solutions and return the best one.
    """
    return dls_helper(start_state, [], 0, max_depth)


def dls_helper(cur_state, actions_so_far, depth, depth_limit):
    """
    Recursive helper function for dls.

    parameters:
    cur_state -- Gamestate
    actions_so_far -- a list of actions that will take you from the
                      start_state (given in dls) to the cur_state.
    depth -- current depth in the search tree
    depth_limit -- do not search in depths that exceed depth_limit.
                   Treat nodes at this depth as leaves.

    Return -- (is_solved, actions) tuple, where is_solved is True or False.
              If is_solved is True, actions = a list of all actions to get form
              start_state (in dfs function) to goal state.
    """
    assert depth <= depth_limit

    if cur_state.is_goal_state():
        return True, actions_so_far

    if depth == depth_limit:
        return False, actions_so_far

    for action in cur_state.get_legal_actions():
        successor = cur_state.get_successor(action)
        actions_so_far.append(action)
        is_solved, actions_to_solution = dls_helper(successor, actions_so_far, depth+1, depth_limit)

        if is_solved:
            return is_solved, actions_to_solution

        prev_action = actions_so_far.pop()
        assert prev_action == action

    return False, actions_so_far

