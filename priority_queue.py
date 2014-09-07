"""
I stole this code from the UC Berkeley Pacman AI projects.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero 
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and 
Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""

import heapq

class PriorityQueue:
    """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it, and the client is usually interested
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
        heapq.heappush(self.heap, pair)

    def pop(self):
        priority, item = heapq.heappop(self.heap)
        return item
  
    def isEmpty(self):
        return len(self.heap) == 0

