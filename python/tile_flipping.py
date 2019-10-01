import random
import queue
import copy

'''
    This is tile-flipping game
    Given a board of black or white tiles
    The goal is to flip the tiles over to get all white tiles
    When you flip a tile, all adjacent tiles are flipped (diagonal?)
'''

# Print out the current state of the board
def print_board(board):
    for row in board:
        print("-", end='')
    print()
    for row in board:
        for item in row:
            print(item, end='')
        print()
    for row in board:
        print("-", end='')
    print()

# Flip a single game board tile x <-> o
def flip_single_tile(x, y, dim, board):
    if x >= 0 and y >= 0 and x < dim and y < dim:
        temp = board[y][x]
        if temp == "x":
            board[y][x] = "o"
        else:
            board[y][x] = "x"

# Flip a tile and all adjacent tiles including diagonals
def flip_tile_diagonal(x, y, dim, board):
    for vx in [x-1, x, x+1]:
        for vy in [y-1, y, y+1]:
            flip_single_tile(vx, vy, dim, board)

# Flip a tile and all adjecent tiles, excluding diagonals
def flip_tile(x, y, dim, board):
    flip_single_tile(x, y, dim, board)
    flip_single_tile(x+1, y, dim, board)
    flip_single_tile(x-1, y, dim, board)
    flip_single_tile(x, y+1, dim, board)
    flip_single_tile(x, y-1, dim, board)

# Assign random values to each space in the baord
def randomize_board(dim, board):
    for x in range(dim):
        for y in range(dim):
            irandom = random.randint(0,1)
            if irandom:
                board[x][y] = "x"
            else:
                board[x][y] = "o"

# Return true if the board is solved, else flase
def solved(board):
    for row in board:
        for item in row:
            if item == "x":
                return False
    return True




def generateBoardFromBinary(dim, l_bin):
    while len(l_bin) < dim*dim:
        l_bin.insert(0, "0")
    # Convert to x, o
    for i in range(len(l_bin)):
        if l_bin[i] == "1":
            l_bin[i] = "x"
        else:
            l_bin[i] = "o"
    # Structure list
    newBoard = [l_bin[i:i+dim] for i in range(0, len(l_bin), dim)]
    return newBoard

def board_to_string(dim, board):
    astring = ""
    for row in board:
        for item in row:
            astring += item
    return astring

# TODO needs to be fixed
def string_to_board(dim, astring):
    board = [astring[i:i+dim] for i in range(0, len(astring), dim)]
    return board

def solvable(dim, board):
    seen_boards = list()
    q = queue.Queue()
    q.put(board)
    while not q.empty():
        board = q.get()
        #print_board(board)
        if solved(board):
            return True
        key = board_to_string(dim, board)
        if key not in seen_boards:
            seen_boards.append(key)
            for x in range(dim):
                for y in range(dim):
                    newBoard = copy.deepcopy(board)
                    flip_tile(x, y, dim, newBoard)
                    q.put(newBoard)
    return False

def all_solvable(dim):
    unsolved = list()
    i_iter = 0
    while i_iter < 2**(dim*dim):
        b_iter = str(bin(i_iter))[2::]
        #print(b_iter)
        l_iter = [b_iter[i] for i in range(len(b_iter))]
        board = generateBoardFromBinary(dim, l_iter)
        print_board(board)
        result = solvable(dim, board)
        print(result)
        if not result:
            unsolved.append(board)
        i_iter += 1

    print(len(unsolved), "arrangments were unsolved")
    for board in unsolved:
        print_board(board)

def play(dim, board):
    while(not solved(board)):
        print_board(board)
        rawInput = input("Pick a tile to flip [x, y]:")
        rawInput = rawInput.split()
        ix = int(rawInput[0])
        iy = int(rawInput[1])
        flip_tile(ix, iy, dim, board)

def all_solvable_2(dim):
    unsolvable = set()
    solvable = set()
    for i_iter in range(2**(dim*dim)):
        b_iter = str(bin(i_iter))[2::]
        l_iter = [b_iter[i] for i in range(len(b_iter))]
        board = generateBoardFromBinary(dim, l_iter)
        print_board(board)
        # Solve specific board
        seen_boards = set()
        q = queue.Queue()
        q.put(board)
        result = False
        while not q.empty():
            board = q.get()
            #print_board(board)
            if solved(board):
                result = True
                break
            key = board_to_string(dim, board)
            if key in solvable:
                result = True
                break
            if key in unsolvable:
                result = False
                break
            if key not in seen_boards:
                seen_boards.add(key)
                for x in range(dim):
                    for y in range(dim):
                        newBoard = copy.deepcopy(board)
                        flip_tile(x, y, dim, newBoard)
                        q.put(newBoard)
        if result:
            solvable |= seen_boards
            while not q.empty():
                solvable.add(board_to_string(dim, q.get()))
        else:
            unsolvable |= seen_boards
            while not q.empty():
                unsolvable.add(board_to_string(dim, q.get()))
        # print(len(solvable))
        # print(len(unsolvable))
        print(result)

    print("Dim:", dim, "Solvable:", len(solvable), "Unsolvable:", len(unsolvable))
    # for board in unsolvable:
    #     print_board(string_to_board(dim, board))

def main():
    dim = 5
    all_solvable_2(dim)
    # Dim: 2 Solvable: 16 Unsolvable: 0
    # Dim: 3 Solvable: 512 Unsolvable: 0
    # Dim: 4 Solvable: 4095 Unsolvable: 61440


main()
