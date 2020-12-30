"""
Run the trapped knight simulation as seen on computerphile
https://www.youtube.com/watch?v=RGQe8waGJ4w
"""

import board
import time

def fill_board(size, mode="center"):
    """Fills a board.Board object with numbers according to the trapped knight problem

    Size is the size of the board, current both x and y
    Mode can either be
    center: fill from a center point spiralling counterclockwise and outwards
    corner: start from the corner, filling diagonally down and left
    """

    if mode == "center":
        #Spiral outwards
        #543
        #612
        #789
        sizex = sizey = size
        b = board.Board((sizex, sizey))
        start = [size // 2, size // 2]
        pos = list(start)

        counter = 1

        side_length = 1

        b[pos[0], pos[1]] = counter
        counter += 1

        max_counter = (size-2)**2
        while counter <= max_counter:
            #Start in center, then spiral right, up, left, down

            #move and fill right
            for _ in range(side_length):
                pos[0] += 1
                b[pos[0], pos[1]] = counter
                counter += 1

            #move and fill up
            for _ in range(side_length):
                pos[1] -= 1
                b[pos[0], pos[1]] = counter
                counter += 1

            side_length += 1

            #move and fill left
            for _ in range(side_length):
                pos[0] -= 1
                b[pos[0], pos[1]] = counter
                counter += 1

            #move and fill down
            for _ in range(side_length):
                pos[1] += 1
                b[pos[0], pos[1]] = counter
                counter += 1

            side_length += 1
        return b

    elif mode == "corner":
        #Start in top left corner, then repeatedly cut down and left across board
        #1247
        #358
        #69
        sizex = sizey = size
        b = board.Board((sizex, sizey))
        start = [0, 0]
        pos = [0, 0]
        corner = [0, 0]
        counter = 1

        while True:
            pos = list(corner)
            while pos[0] >= 0:
                if (pos[0], pos[1]) not in b:
                    #if upper corner is not in our board, we are down filling
                    #b.draw()
                    return b
                b[pos[0], pos[1]] = counter
                counter += 1
                pos[0] -= 1
                pos[1] += 1
            corner[0] += 1

def knights_journey(b, start):
    """Repeatedly move knight to the lowest, unvisited square

    b: filled board
    start: starting position of knight
    Movement is knight is that of chess, moving 1 square in one coordinate and 2 in the other
    This function will run until the knight is no longer able to move,
    """

    ob = b.copy()
    pos = list(start)
    visited = 9999 #How we demarcate visited squares, so min won't choose them
    list_of_pos = [list(start)]

    b[pos[0], pos[1]] = visited

    for i in range(5000):
        next_pos = [] # list of possible new positions
        for x in [-2, 2]:
            for y in [-1, 1]:
                temp_pos = list(pos)
                temp_pos[0] += x
                temp_pos[1] += y
                next_pos.append(temp_pos)
        for x in [-1, 1]:
            for y in [-2, 2]:
                temp_pos = list(pos)
                temp_pos[0] += x
                temp_pos[1] += y
                next_pos.append(temp_pos)

        #remove positions that go off the board (only an issue in starting in the corner)
        for i in range(len(next_pos)-1, -1, -1): # run backwards to avoid delete issues
            if next_pos[i][0] < 0 or next_pos[i][1] < 0:
                del(next_pos[i])

        #Pick min position
        min_pos = []
        min_val = float("inf")
        for p in next_pos:
            val = b[p[0], p[1]]
            if val < min_val:
                min_pos = list(p)
                min_val = val

        #If min position is visited, knight is stuck
        if b[min_pos[0], min_pos[1]] == visited:
            b.draw()
            print("I am stuck!")
            break
        list_of_pos.append(min_pos)
        b[min_pos[0], min_pos[1]] = "h"
        pos = list(min_pos)
        #time.sleep(1)
        #b.draw()
        b[min_pos[0], min_pos[1]] = visited

    print("List of positions coordinates")
    print(list_of_pos)
    vals = [ob[x[0], x[1]] for x in list_of_pos]
    print("List of position values")
    print(vals)

def main():
    # Run the program with the center version
    size = 63 #min boardsize needed to solve problem
    b = fill_board(size, mode = "center")
    start = [size // 2, size // 2]
    knights_journey(b, start)

    # Run the program with the corner version
    size = 89 #min boardsize needed to solve problem
    b = fill_board(size, mode = "corner")
    start = [0,0]
    knights_journey(b, start)

#TODO consider refactoring into a more Object Oriented design to allow for experimentation
#Better visualization, specifically drawing the line, LIVE
#

main()
