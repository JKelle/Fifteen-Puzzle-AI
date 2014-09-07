
__author__ = "Josh Kelle"

correct_locations = {
                      1: (0, 0),   2: (0, 1),   3: (0, 2),   4: (0, 3),
                      5: (1, 0),   6: (1, 1),   7: (1, 2),   8: (1, 3),
                      9: (2, 0),  10: (2, 1),  11: (2, 2),  12: (2, 3),
                     13: (3, 0),  14: (3, 1),  15: (3, 2),  16: (3, 3)
                    }

class Gamestate(object):

    """
    This class represents a single state of the game board.
    Uses a 2D (4 x 4) list of integers 1 - 16.
    16 represents the blank tile.
    """

    def __init__(self, grid):
        """
        Contructor

        parameters:
        grid -- a 2D (4 x 4) list of ints
        """
        # convert to tuples to 1) ensure the state doesn't change
        #                  and 2) make the hash function quick
        self.grid = tuple(map(tuple, grid))

        # remember position of blank tile to make legal move checking quick
        self.blank_loc = self._find_16()

    def get_successor(self, action):
        """
        Generate a new Gamestate that would result from taking a given
        action on this Gamestate.

        parameters:
        action -- a 2-tuple specifying which tile to "click."
                  Must be adjacent to the blank tile (#16).

        return:
        Return a new Gamestate object.
        """
        assert self._is_legal_action(action)

        row, col = action
        blank_row, blank_col = self.blank_loc
        
        new_grid = [list(row_) for row_ in self.grid]
        new_grid[blank_row][blank_col] = new_grid[row][col]
        new_grid[row][col] = 16

        return Gamestate(new_grid)
        #return Gamestate(new_grid, (row, col))

    def get_legal_actions(self):
        """
        Return a list of all posible actions actions. An action is a tile
        location which a player touches to move. So the action must be next
        to the blank tile.

        return:
        Return a list of 2-tuples of integers.
        """
        # slow
        actions = [(r, c) for r in range(4) for c in range(4) if self._is_legal_action((r,c))]
        assert len(actions) in (2, 3, 4)
        return actions

    def is_goal_state(self, targets=range(1,17)):
        """
        Return True if all targets are in their correct locations.

        parameters:
        targets -- a list of (row, col) int tuples.
                   This allows the client to define what a goal state is.
                   By changing targets, the client can detect, for example,
                   when only the first 4 tiles are in the right place.
                   Defaults to all 16 tiles.
        """
        for row in range(4):
            for col in range(4):
                num = self.grid[row][col]
                if num in targets and correct_locations[num] != (row, col):
                    return False

        return True

    def print_board(self):
        """
        Display the board as a 4 x 4 grid of integers.
        """
        print "\n".join(["".join(["%3d" % num for num in row]) for row in self.grid]) + "\n"

    def _is_legal_action(self, (row, col)):
        """
        Make sure a given location is 1) a valid location on the board,
        and 2) next to the blank tile.

        parameters:
        (row, col) -- 2-tuple of integers

        return:
        Return True or False
        """
        if not 0 <= row <= 3 or not 0 <= col <= 3:
            return False

        blank_row, blank_col = self.blank_loc
        return (row == blank_row and abs(col - blank_col) == 1) or \
               (col == blank_col and abs(row - blank_row) == 1)

    def _find_16(self):
        """
        Return the (row, col) position of the blank tile.
        This method should only be called once - in the constuctor.
        """
        for row in range(4):
            for col in range(4):
                if self.grid[row][col] == 16:
                    return row, col

        raise Exception("16 not found")

    def __hash__(self):
        return hash(self.grid)

    def __eq__(self, other):
        return other.grid == self.grid

if __name__ == '__main__':
    board = Gamestate([[ 1,  2,  3,  4], 
                       [ 5, 16,  6,  8], 
                       [ 9, 14,  7, 11], 
                       [13, 15, 10, 12]])
