import time
import heapq
import copy
import unittest
from pprint import pprint

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
        
        new_grid = copy.deepcopy(self.grid)
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

goal_grid = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]

def is_goal_state(gamestate, targets):
    grid = gamestate.grid

    for row in range(4):
        for col in range(4):
            num = grid[row][col]
            if num in targets and correct_locations[num] != (row, col):
                return False

    return True

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

def astar(start_gamestate, heuristic_func, targets):
    start_time = time.time()
    cur_state = start_gamestate
    cur_actions = []
    prev_len = -1

    fringe = PriorityQueue()
    visited_states = set()

    while not is_goal_state(cur_state, targets):
        if len(cur_actions) > prev_len:
            print len(cur_actions), time.time() - start_time
            prev_len = len(cur_actions)
        visited_states.add(cur_state)

        for action in cur_state.get_legal_actions():
            successor = cur_state.get_successor(action)
            if successor not in visited_states:
                priority = len(cur_actions) + 1 + heuristic_3(cur_state, targets)
                fringe.push( (successor, cur_actions + [action]), priority )

        next_state, actions_to_next_state = fringe.pop()
        while next_state in visited_states:
            next_state, actions_to_next_state = fringe.pop()

        cur_actions = actions_to_next_state
        cur_state = next_state

    return cur_actions, cur_state

def bfs(start_gamestate):
    start_time = time.time()
    cur_state = start_gamestate
    cur_actions = []
    prev_len = -1

    fringe = Queue()
    visited_states = set()

    while not is_goal_state(cur_state):
        if len(cur_actions) > prev_len:
            print len(cur_actions), time.time() - start_time
            prev_len = len(cur_actions)
        visited_states.add(cur_state)

        for action in cur_state.get_legal_actions():
            successor = cur_state.get_successor(action)
            if successor not in visited_states:
                fringe.push( (successor, cur_actions + [action]) )

        next_state, actions_to_next_state = fringe.pop()
        while next_state in visited_states:
            next_state, actions_to_next_state = fringe.pop()

        cur_actions = actions_to_next_state
        cur_state = next_state

    return cur_actions

#################
#  stolen code  #
#################

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []
    
    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
        Dequeue the earliest enqueued item still in the queue. This
        operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

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
        astar_result = astar(start_state)
        bfs_result = bfs(start_state)
        answer = []

        self.assertTrue(astar_result == answer == bfs_result)

    def test_2(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,16,15]])
        astar_result = astar(start_state)
        bfs_result = bfs(start_state)
        answer = [(3,3)]

        self.assertTrue(astar_result == answer == bfs_result)
    
    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,16,14,15]])
        astar_result = astar(start_state)
        bfs_result = bfs(start_state)
        answer = [(3,2),(3,3)]

        self.assertTrue(astar_result == answer == bfs_result)

    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7,16],
                                 [ 9,10,11, 8],
                                 [13,14,15,12]])
        astar_result = astar(start_state)
        bfs_result = bfs(start_state)
        answer = [(2,3),(3,3)]

        self.assertTrue(astar_result == answer == bfs_result)

    def test_4(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,16,11],
                                 [13,14,15,12]])
        astar_result = astar(start_state)
        bfs_result = bfs(start_state)
        answer = [(2,3),(3,3)]

        self.assertTrue(astar_result == answer == bfs_result)

if __name__ == '__main__':
    #unittest.main()
    #def goal_func_12(gamestate):
    #    return gamestate.grid[0][0] == 1 and gamestate.grid[0][1] == 2
    #def goal_func_34(gamestate):
    #    return goal_func_21(gamestate) and gamestate.grid[0][2] == 3 and gamestate.grid[0][3] == 4
    
    nums = [1,2,3,4,   5,16,6,8,   9,14,7,11,  13,15,10,12]
    nums = [8,4,5,7, 13,3,2,14, 11,15,10,9, 12,16,1,6]
    start_grid = [nums[0:4], nums[4:8], nums[8:12], nums[12:16]]
    start_state = Gamestate(start_grid)

    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"
    print

    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2,3,4]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"

    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2,3,4,5,6]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"

    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2,3,4,5,6,7,8]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"
    
    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2,3,4,5,6,7,8,9,13]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"
    
    actions, end_state = astar(start_state, heuristic_3, targets=set([1,2,3,4,5,6,7,8,9,13,10,11,12,14,15,16]))
    #actions = bfs(start_state)
    pprint(actions)
    pprint(end_state.grid)
    print len(actions), "moves"

