import time
import heapq
import copy
import unittest
from pprint import pprint

class Gamestate(object):

    def __init__(self, grid, blank_loc=None):
        """
        parameters:
        nums -- a list of 16 integers (1 - 16).
                read from the board row major, left to right.
                16 is the blank spot.

                 4  5 15 11
                 9  7  2  3  ->  [4, 5, 15, 11, 9, 7, 2, ..., 1, 16]
                12  8  6 13
                14 10  1 16  !NO LONGER ACCURATE!
        """
        #assert sorted(nums) == goal

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

def is_goal_state(gamestate):
    return gamestate.grid == goal_grid

def search(start_gamestate):
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
        result = search(start_state)
        answer = []

        self.assertTrue(result == answer)

    def test_2(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,16,15]])
        result = search(start_state)
        answer = [(3,3)]

        self.assertTrue(result == answer)
    
    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,16,14,15]])
        result = search(start_state)
        answer = [(3,2),(3,3)]
        print result

        self.assertTrue(result == answer)

    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7,16],
                                 [ 9,10,11, 8],
                                 [13,14,15,12]])
        result = search(start_state)
        answer = [(2,3),(3,3)]
        print result

        self.assertTrue(result == answer)

    def test_4(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,16,11],
                                 [13,14,15,12]])
        result = search(start_state)
        answer = [(2,3),(3,3)]
        print result

        self.assertTrue(result == answer)

if __name__ == '__main__':
    unittest.main()
    
    nums = [1,2,3,4,   5,16,6,8,   9,14,7,11,  13,15,10,12]
    start_grid = [nums[0:4], nums[4:8], nums[8:12], nums[12:16]]
    start_state = Gamestate(start_grid)

    actions = search(start_state)
    pprint(actions)
    print len(actions), "moves"

