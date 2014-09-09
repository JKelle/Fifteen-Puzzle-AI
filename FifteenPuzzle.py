
__author__ = "Dallas Kelle, Josh Kelle"

from Tkinter import *
import time
from random import randint
import random
import copy
from tile import Tile
from pprint import pprint

from gamestate import Gamestate
import fifteen_puzzle_ai

WIDTH = 325
HEIGHT = 450

startingx = 20
sqlength = (WIDTH - startingx * 2.0) / 4.0

board = None
canvas = None

tilesMoving = False

lastScramble = (0,0)

def init(master):
    global board, canvas
    
    canvas = Canvas(master, width=WIDTH, height=HEIGHT, bg='WHITE')
    canvas.pack()

    board =[[],[],[],[]]
    for rowindex, row in enumerate(board):
        for i in range(1,5):
            board[rowindex].append(Tile(rowindex*4+i))

    board[-1][-1] = None
    
    initTime = time.time()  
    initboard()

def initboard():
    canvas.create_rectangle(startingx, startingx, WIDTH - startingx, WIDTH - startingx)

    # Want highlighted bottom edge?
    for rowindex, tiles in enumerate(board):
        for colindex, tile in enumerate(tiles):
            if tile == None:
                continue
            x = startingx + colindex * sqlength
            y = startingx + sqlength * rowindex
            canvas.create_rectangle(x, y, x + sqlength, y + sqlength, tag='tile'+str(tile.getNumber()))
            canvas.create_text(x + sqlength / 2, y + sqlength / 2, text=tile.getNumber(), tag = 'text'+str(tile.getNumber()))

    canvas.create_rectangle(startingx, WIDTH, startingx + (WIDTH - 2*startingx) / 2 - 10,  WIDTH + 40)
    canvas.create_text((WIDTH - 2*startingx) / 4 + startingx, WIDTH + 20, text='scramble')

    canvas.create_rectangle(startingx + (WIDTH - 2*startingx) / 2 + 10, WIDTH, WIDTH - startingx, WIDTH + 40)
    canvas.create_text((WIDTH - 2*startingx) / 4 * 3 + startingx, WIDTH + 20, text='PIZZA')
    canvas.bind('<Button-1>', clicked)
    canvas.create_text(WIDTH/2, 400, text = "", tag = "boardtext")


def change_board_text(text):
    canvas.itemconfig("boardtext", text = text)

def draw_time_and_moves(time, num_moves):
    canvas.delete("solving")
    canvas.create_text(WIDTH/2, 400,
                       text="solved in %d moves\n(%.2f seconds)" % (num_moves, time),
                       tag="time_and_moves")

def draw_solving():
    canvas.delete("time_and_moves")
    canvas.create_text(WIDTH/2, 400,
                       text="solving...",
                       tag="solving")

def clicked(event):
    c = int((event.x - startingx) / sqlength)
    r = int((event.y - startingx) / sqlength)

    print 'r,c',r,c

    #Clicked 'scramble'
    if r  == 4 and c < 2:
        print 'scrambling'
        scramble(20)

    if r == 4 and c >= 2 and c < 4:
        solve()
        #pizza()

    #Clicked a tile
    if r < len(board) and r >= 0 and c < len(board[0]) and c >= 0:
        #didn't click empty tile
        if not board[r][c] == None and (r,c) in getNeighbors(getBlankLocation()):
            makeMove((r, c), .2)

def makeMove((r, c), secondsToMove):
    """
    parameters:
    r, c -- position to move blank tile to
    secondsToMove -- ...
    """
    blankRow, blankCol = getBlankLocation()
    x, y = blankCol - c, blankRow - r

    temptile = board[r][c]
    board[r][c] = None
    board[r+y][c+x] = temptile

    r += y
    c += x

    starttime = time.time()
    prevtime = starttime
    now = prevtime + .00000001 # don't divide by zero
    dx = 0
    tilenumber = str(board[r][c].getNumber())

    while(now - starttime < secondsToMove):
        now = time.time()
        dt = now - prevtime
        move = sqlength/(secondsToMove/dt)
        
        if dx + move > sqlength:
            move = sqlength - dx
        dx += sqlength/(secondsToMove/dt)

        canvas.move('tile'+tilenumber, move * x, move * y)
        canvas.move('text'+tilenumber, move * x, move * y)
        
        prevtime = now
        canvas.update()

def scramble(num_moves=100):
    global tilesMoving
    if tilesMoving:
        return
    change_board_text("Scrambling with "+str(num_moves)+" moves.")
    tilesMoving = True
    lastScramble = None
    for i in range(num_moves):
        lastScramble = one_move(lastScramble)
    tilesMoving = False
    change_board_text("")

def one_move(lastScramble=None):
    """
    1. find blank location
    2. board.getNeighbors()
    3. take out lastScramble
    4. randomly choose form remaining neighbors
    5. update location of blank tile - optional
    """
    blankLoc = getBlankLocation()
    
    neighbors = getNeighbors(blankLoc)
    neighbors = [neighbor for neighbor in neighbors if neighbor != lastScramble]
    makeMove(random.choice(neighbors), .06)
    
    return blankLoc

def getNeighbors((row, col)):
    allNeighbors = [(row-1, col),
                    (row+1, col),
                    (row,   col-1),
                    (row,   col+1)]

    return filter(isLegalPosition, allNeighbors)

def getBlankLocation():
    """
    Return a (row, col) tuple which is the location of the blank tile.
    """
    for r, tiles in enumerate(board):
        for c, tile in enumerate(tiles):
            if tile == None:
                return r, c

def isLegalPosition((row, col)):
    return 0 <= row <= 3 and 0 <= col <= 3

def solve():
    global tilesMoving
    if tilesMoving:
        return
    else:
        tilesMoving = True
    change_board_text("Solving...")
    nums = board_to_nums()

    start_state = Gamestate(nums)

    #draw_solving()
    
    start_time = time.time()
    actions = fifteen_puzzle_ai.solve_astar_7breaks(start_state)
    elapsed_time = time.time() - start_time

    pizza()

    change_board_text("Solved in "+ str(elapsed_time)[:4]+" seconds and " + str(len(actions)) +" moves.")
    #draw_time_and_moves(elapsed_time, len(actions))

    for action in actions:
        makeMove(action, 0.15)
    tilesMoving = False

def board_to_nums():
    board_ = []
    for r in range(4):
        row = []

        for c in range(4):
            if board[r][c] is None:
                num = 16
            else:
                num = board[r][c].getNumber()

            row.append(num)

        board_.append(row)

    return board_

def pizza():
    pizza = """

        ____________________
        \__________________/
         \  (_)      (_)  /
          \       _      /
           \     (_)  _ /
            \  _     (_/
             \(_)     / 
              \   _  /
               \ (_)/
                \  /
                 \/

    """

    print pizza

def main():
    master = Tk()
    init(master)
    master.mainloop()

if __name__ == '__main__':
    main()

