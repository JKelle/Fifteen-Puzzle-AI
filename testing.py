import unittest
from gamestate import Gamestate
from search import *

"""
Acceptance tests for solving the fifteens puzzle game.
"""

class Tests(unittest.TestCase):

    def test_1(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,15,16]])
        actions, end_state = astar(start_state, q=True)
        correct_actions = []

        self.assertTrue(actions == correct_actions)
        self.assertTrue(end_state.is_goal_state())

    def test_2(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,14,16,15]])
        actions, end_state = astar(start_state, q=True)
        correct_actions = [(3,3)]

        self.assertTrue(actions == correct_actions)
        self.assertTrue(end_state.is_goal_state())
    
    def test_3(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,11,12],
                                 [13,16,14,15]])
        actions, end_state = astar(start_state, q=True)
        correct_actions = [(3,2),(3,3)]

        
        self.assertTrue(actions == correct_actions)
        self.assertTrue(end_state.is_goal_state())

    def test_4(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7,16],
                                 [ 9,10,11, 8],
                                 [13,14,15,12]])
        actions, end_state = astar(start_state, q=True)
        correct_actions = [(2,3),(3,3)]

        
        self.assertTrue(actions == correct_actions)
        self.assertTrue(end_state.is_goal_state())

    def test_5(self):
        start_state = Gamestate([[ 1, 2, 3, 4],
                                 [ 5, 6, 7, 8],
                                 [ 9,10,16,11],
                                 [13,14,15,12]])
        actions, end_state = astar(start_state, q=True)
        correct_actions = [(2,3),(3,3)]

        self.assertTrue(actions == correct_actions)
        self.assertTrue(end_state.is_goal_state())

if __name__ == '__main__':
	unittest.main()

	