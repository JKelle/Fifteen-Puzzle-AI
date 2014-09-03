import time
import heapq
import copy
import unittest
from pprint import pprint

correct_locations = {
                     1: (0, 0),
                     2: (0, 1),
                     3: (0, 2),
                     4: (0, 3),

                     5: (1, 0),
                     6: (1, 1),
                     7: (1, 2),
                     8: (1, 3),

                      9: (2, 0),
                     10: (2, 1),
                     11: (2, 2),
                     12: (2, 3),

                     13: (3, 0),
                     14: (3, 1),
                     15: (3, 2),
                     16: (3, 3),
                    }

class Gamestate(object):

    def __init__(self, grid, blank_loc=None):
        self.grid = grid

        if blank_loc is None:
            self.blank_loc = self._find_16()
        else:
            self.blank_loc = blank_loc

    def get_successor(self, action):
        """
        Generate a new Gamestate that would result from taking a given
        action on this Gamestate.

        parameters:
        action -- a 2-tuple specifying which tile to "click"
                  (row, column), 0 <= row <= 3
                  must be adjacent to the blank tile (#16)

        return:
        Return a new Gamestate object.
        """
        assert self._is_legal_action(action)

        row, col = action
        blank_row, blank_col = self.blank_loc
        
        new_grid = [row_[:] for row_ in self.grid]
        new_grid[blank_row][blank_col] = new_grid[row][col]
        new_grid[row][col] = 16

        return Gamestate(new_grid, (row, col))

    def get_legal_actions(self):
        actions = [(r, c) for r in range(4) for c in range(4) if self._is_legal_action((r,c))] # slow
        assert len(actions) in (2, 3, 4)
        return actions

    def _is_legal_action(self, (row, col)):
        if not 0 <= row <= 3 or not 0 <= col <= 3:
            return False

        blank_row, blank_col = self.blank_loc # slow
        return (row == blank_row and abs(col - blank_col) == 1) or \
               (col == blank_col and abs(row - blank_row) == 1)

    def _find_16(self):
        """
        :(
        """
        print "_find_16"

        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 16:
                    return row, col

        raise Exception("16 not found")

    def __hash__(self):
        tuple_form = tuple(map(tuple, self.grid))
        return hash( tuple_form )

    def __eq__(self, other):
        return other.grid == self.grid

    def print_board(self):
        print "\n".join(["".join(["%3d" % num for num in row]) for row in self.grid]) + "\n"

def is_goal_state(gamestate, targets=range(1,17)):
    grid = gamestate.grid

    for row in range(4):
        for col in range(4):
            num = grid[row][col]
            if num in targets and correct_locations[num] != (row, col):
                return False

    return True

##############
# heuristics #
##############

def dist((a,b), (x,y)):
    return abs(a-x) + abs(b-y)

def heuristic_0(gamestate):
    return 0

def heuristic_1(gamestate):
    grid = gamestate.grid
    cost = 0
    if grid[0][0] != 1:
        cost += 1
    if grid[0][1] != 2:
        cost += 1
    if grid[0][2] != 3:
        cost += 1
    if grid[0][3] != 4:
        cost += 1

    if grid[1][0] != 5:
        cost += 1
    if grid[1][0] != 6:
        cost += 1
    if grid[1][1] != 7:
        cost += 1
    if grid[1][2] != 8:
        cost += 1

    if grid[2][0] != 9:
        cost += 1
    if grid[2][0] != 10:
        cost += 1
    if grid[2][1] != 11:
        cost += 1
    if grid[2][2] != 12:
        cost += 1

    if grid[3][0] != 13:
        cost += 1
    if grid[3][0] != 14:
        cost += 1
    if grid[3][1] != 15:
        cost += 1
    if grid[3][2] != 16:
        cost += 1

    return cost

def heuristic_2(gamestate):
    global correct_locations
    grid = gamestate.grid
    cost = 0

    for row in range(4):
        for col in range(4):
            cost += dist((row, col), correct_locations[grid[row][col]])

    return cost

def heuristic_3(gamestate, targets):
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

def astar(start_gamestate, heuristic_func=heuristic_3, targets=range(1,17), q=False):
    start_time = time.time()
    cur_state = start_gamestate
    cur_actions = []
    prev_len = -1

    fringe = PriorityQueue()
    visited_states = set()

    while not is_goal_state(cur_state, targets):
        
        # print info to the screen
        # doesn't actually do anything for the search
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
                # h = heuristic_func
                priority = len(cur_actions) + 1 + heuristic_func(cur_state, targets)
                fringe.push( (successor, cur_actions + [action]), priority )

        # get next state from fringe, skipping ones we've seen already
        next_state, actions_to_next_state = fringe.pop()
        while next_state in visited_states:
            next_state, actions_to_next_state = fringe.pop()

        cur_actions = actions_to_next_state
        cur_state = next_state

    return cur_actions, cur_state

######################
# depth first search #
######################

def dfs(start_state):
    is_solved, actions_to_solution = dfs_helper(start_state, actions_so_far=[])

    assert is_solved
    return actions_to_solution

def dfs_helper(cur_state, actions_so_far):
    """
    return -- (is_solved, actions) tuple, where is_solved is True or False.
              If is_solved is True, actions = a list of all actions to get form
              start_state (in dfs function) to goal state.
    """
    if is_goal_state(cur_state):
        return True, actions_so_far

    for action in cur_state.get_legal_actions():
        successor = cur_state.get_successor(action)
        actions_so_far.append(action)
        is_solved, actions_to_solution = dfs_helper(successor, actions_so_far)

        if is_solved:
            return is_solved, actions_to_solution

        prev_action = actions_so_far.pop()
        assert prev_action == action

    return False, actions_so_far

########################
# depth limited search #
########################

#########
# solve #
#########

def solve_astar(start_state):
    start_time = time.time()
    targets_list = [[1, 2],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4, 5, 6],
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    all_actions = []
    cur_state = start_state

    for targets in targets_list:
        cur_state.print_board()
        actions, cur_state = astar(cur_state, heuristic_3, targets, q=True)
        all_actions += actions

    cur_state.print_board()
    assert is_goal_state(cur_state, range(1,17))

    print len(all_actions), "moves"
    print "solved in %s seconds" % (time.time() - start_time)

    return all_actions

def solve_dfs(start_state):
    start_time = time.time()

    actions = dfs(start_state)

    print len(actions), "moves"
    print "solved in %s seconds" % (time.time() - start_time)

    return actions

#################
#  stolen code  #
#################

class PriorityQueue:
    """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.
    
    Note that this PriorityQueue does not allow you to change the priority
    of an item.  However, you may insert the same item multiple times with
    different priorities.
    """  
    def  __init__(self):  
        self.heap = []
    
    def push(self, item, priority):
        pair = (priority,item)
        heapq.heappush(self.heap,pair)

    def pop(self):
        (priority,item) = heapq.heappop(self.heap)
        return item
  
    def isEmpty(self):
        return len(self.heap) == 0

###########
#  tests  #
###########

class Tests(unittest.TestCase):

    def test_1(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,15,16]])
        actions, end_state = astar(start_state)
        correct_actions = []

        self.assertTrue(actions == correct_actions)
        self.assertTrue(is_goal_state(end_state, range(1,17)))

    def test_2(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,16,15]])
        actions, end_state = astar(start_state)
        correct_actions = [(3,3)]

        self.assertTrue(actions == correct_actions)
        self.assertTrue(is_goal_state(end_state, range(1,17)))
    
    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,16,14,15]])
        actions, end_state = astar(start_state)
        correct_actions = [(3,2),(3,3)]

        
        self.assertTrue(actions == correct_actions)
        self.assertTrue(is_goal_state(end_state, range(1,17)))

    def test_4(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7,16],
                                 [ 9,10,11, 8],
                                 [13,14,15,12]])
        actions, end_state = astar(start_state)
        correct_actions = [(2,3),(3,3)]

        
        self.assertTrue(actions == correct_actions)
        self.assertTrue(is_goal_state(end_state, range(1,17)))

    def test_5(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,16,11],
                                 [13,14,15,12]])
        actions, end_state = astar(start_state)
        correct_actions = [(2,3),(3,3)]

        self.assertTrue(actions == correct_actions)
        self.assertTrue(is_goal_state(end_state, range(1,17)))

if __name__ == '__main__':
    #unittest.main()
    
    # 8/8 moves
    #solve_astar( Gamestate([[1,2,3,4], [5,16,6,8], [9,14,7,11], [13,15,10,12]]) )
    solve_dfs( Gamestate([[1,2,3,4], [5,16,6,8], [9,14,7,11], [13,15,10,12]]) ) 
    
    # 77/71 moves
    #solve_astar( Gamestate([[7,14,1,13], [4,5,12,10], [2,6,3,8], [16,15,11,9]]) )

    # 68/62 moves
    #solve_astar( Gamestate([[7,3,16,15], [6,5,4,10], [2,11,14,13], [9,1,12,8]]) )

    # 77/55 moves
    #solve_astar( Gamestate([[14,16,4,9], [13,2,7,12], [3,1,6,8], [10,15,5,11]]) )    

    