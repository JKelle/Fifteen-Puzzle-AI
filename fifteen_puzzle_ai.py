
__author__ = "Josh Kelle"

import search
from gamestate import Gamestate
import time
from pprint import pprint

##################
#  A* solutions  #
##################

def solve_astar_7breaks(start_state):
    targets_list = [[1, 2],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4, 5, 6],
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar_6breaks(start_state):
    targets_list = [[1, 2],
                    [1, 2, 3, 4],
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar_5breaks(start_state):
    targets_list = [[1, 2, 3, 4],
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar_4breaks(start_state):
    targets_list = [[1, 2, 3, 4],
                    [1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar_2breaks(start_state):
    targets_list = [[1, 2, 3, 4, 5, 6, 7, 8],
                    [1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar_1breaks(start_state):
    targets_list = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 14, 11, 12, 15, 16]]

    return solve_astar(start_state, targets_list)

def solve_astar(start_state, targets_list):
    start_time = time.time()

    assert type(start_state)        is Gamestate
    assert type(targets_list)       is list
    assert type(targets_list[0])    is list
    assert type(targets_list[0][0]) is int

    all_actions = []
    cur_state = start_state

    for targets in targets_list:
        actions, cur_state = search.astar(cur_state, search.heuristic_3, targets, q=True)
        all_actions += actions
        cur_state.print_board()

    cur_state.print_board()
    assert cur_state.is_goal_state()

    print len(all_actions), "moves"
    print "solved in %s seconds" % (time.time() - start_time)

    return all_actions

####################################
#  depth limited search solutions  #
####################################

def solve_dls(start_state):
    start_time = time.time()

    actions = search.iterative_deepening_dfs(start_state)

    print len(actions), "moves"
    print "solved in %s seconds" % (time.time() - start_time)

    return actions

#######################
#  compare solutions  #
#######################

def compare_astar_and_dls(start_state):
    """
    Compare different solutions.

    The more coponents you break the game into, the faster it's solved, but
    it becomes further from optimal.

    Depth limited/iterative deepening takes too long.
    """
    astar7_actions = solve_astar_7breaks(start_state)
    astar5_actions = solve_astar_5breaks(start_state)
    astar4_actions = solve_astar_4breaks(start_state)
    dls_actions   = solve_dls(start_state)

    print "astar7 %d moves" % len(astar7_actions)
    print "astar5 %d moves" % len(astar5_actions)
    print "astar4 %d moves" % len(astar4_actions)
    print "dls    %d moves" % len(dls_actions)
    print "~" * 80

if __name__ == '__main__':
    sstate_1 = Gamestate([[1,2,3,4], [5,16,6,8], [9,14,7,11], [13,15,10,12]]) #  8  8  8  8
    sstate_2 = Gamestate([[7,14,1,13], [4,5,12,10], [2,6,3,8], [16,15,11,9]]) # 77 71 71  ?
    sstate_3 = Gamestate([[7,3,16,15], [6,5,4,10], [2,11,14,13], [9,1,12,8]]) # 68 78 62  ?
    sstate_4 = Gamestate([[14,16,4,9], [13,2,7,12], [3,1,6,8], [10,15,5,11]]) # 87 55 55  ?
    
    #compare_astar_and_dls(sstate_1)
    #compare_astar_and_dls(sstate_2)
    #compare_astar_and_dls(sstate_3)
    compare_astar_and_dls(sstate_4)

    # 77/55 moves

    