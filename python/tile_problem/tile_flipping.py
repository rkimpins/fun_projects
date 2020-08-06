import random
import queue
import copy

"""
    This is tile-flipping game
    Given a board of black or white tiles
    The goal is to flip the tiles over to get all white tiles
    When you flip a tile, all adjacent tiles are flipped, but not the diagonals
    I was curious what configurations were solvable, and what the solution to them was
    So using a simple breadth first search, we find the optimal solution
    (if it exists)
"""

# Assign random values to each space in the baord
def randomize_board(dim):
    """ Assign 0 or 1 randomly to tile on the board """
    board = list()
    for i in range(dim**2):
        irandom = random.randint(0,1)
        board.append(str(irandom))
    return "".join(board)

def play(dim, board):
    """ Play an instance of the game with a given board """
    while(not solved(board)):
        print_board(board)
        rawInput = input("Pick a tile to flip [x, y]:")
        rawInput = rawInput.split()
        ix = int(rawInput[0])
        iy = int(rawInput[1])
        flip_tile(ix, iy, dim, board)

def is_goal(board):
    """ Return true if the state is the end state of our problem (all zeros) """
    for item in list(board):
        if item == "1":
            return False
    return True

def flip_tile(x, y, dim, board):
    """ Flip a single tile on our board, not including the adjacent ones """
    if x < 0 or y < 0 or x >= dim or y >= dim:
        return board
    else:
        lboard = list(board)
        temp = lboard[x + dim*y]
        if temp == "1":
            lboard[x + dim*y] = "0"
        else:
            lboard[x + dim*y] = "1"
        board = "".join(lboard)
        return board

def flip_tile_set(x, y, dim, board):
    """ Flip a single tile on our board, and the adjacent tiles """
    board = flip_tile(x, y, dim, board)
    board = flip_tile(x+1, y, dim, board)
    board = flip_tile(x-1, y, dim, board)
    board = flip_tile(x, y+1, dim, board)
    board = flip_tile(x, y-1, dim, board)
    return board

def print_board(dim, board, sym1="0", sym2="1", sym_top="-", sym_bot="-", sym_left="|", sym_right="|"):
    """ Print our board in a pretty fashion """
    board = list(board)
    print(sym_top * (dim+2))
    for x in range(0, dim):
        print(sym_left, end = '')
        for y in range(0, dim):
            if board[x+dim*y] == 0:
                print(sym1, end='')
            else:
                print(sym2, end='')
        print(sym_right)
    print(sym_bot * (dim+2))

def solve(dim, board, solvable=set(), unsolvable=set(), silent = False):
    """ For a given configuration of the board, return if it is solvable

    solvable and unsolvable are sets that we pass in. They store intermediate
    solvable or unsovable configurations. This drastically cuts down
    performance time when solving mulitiple puzzles of the same dimension
    silent means we don't print anything, like when we are running many puzzles
    """
    seen = set()
    frontier = queue.Queue()
    path = [board]
    frontier.put(path)
    while not frontier.empty():
        path = frontier.get()
        board = path[-1]
        if is_goal(board):
            if not silent:
                print(f"Solution found in {len(path)} steps")
                for board in path:
                    print_board(dim, board)
            return True, path, seen
        if board in solvable:
            return True, path, seen
        if board in unsolvable:
            return False, None, seen
        for x in range(dim):
            for y in range(dim):
                newPath = copy.deepcopy(path)
                newBoard = newPath[-1]
                newBoard = flip_tile_set(x, y, dim, newBoard)
                newPath.append(newBoard)
                if newBoard not in seen:
                    frontier.put(newPath)
                    seen.add(newBoard)
    return False, None, seen

def bin_to_string(dim, l_bin):
    """ Convert a binary string to a baord state. Used for iterating over all puzzles """
    while len(l_bin) < dim*dim:
        l_bin.insert(0, "0")
    return "".join(l_bin)

def all_solvable(dim):
    """ For a given dimension, checks if solvable for every possible board configuration """
    solvable = set()
    unsolvable = set()
    unsolved_boards = list()
    solved_boards = list()
    i_iter = 0
    while i_iter < 2**(dim*dim):
        b_iter = str(bin(i_iter))[2::]
        l_iter = [b_iter[i] for i in range(len(b_iter))]
        board = bin_to_string(dim, l_iter)

        solved, path, seen = solve(dim, board, solvable, unsolvable, silent=True)

        if solved:
            solvable |= seen
            solved_boards.append(board)
        else:
            unsolvable |= seen
            unsolved_boards.append(board)
        i_iter += 1
    print("Solved Configurations")
    for board in solved_boards:
        print_board(dim, board)
    print("Unsolvable Configurations")
    for board in unsolved_boards:
        print_board(dim, board)
    print(f"Dim: {dim}, Solvable: {len(solved_boards)}, Unsolvable: {len(unsolved_boards)}")

def main():
    # A nice bash command to run the program and see results
    # touch test.txt && rm test.txt && python3 tile_flipping.py >> test.txt && vim test.txt

    # Check all solutions for a certain dimension
    all_solvable(4)

    # Example of solving a simple problem
    # board = "100011001"
    # dim = 3
    # solve(dim, board)


    '''
    Some intersting results
    +-----+-------------+----------+------------+
    | Dim | States      | Solvable | Unsolvable |
    +=====+=============+==========+============+
    | 1   | 1           | 1        | 0          |
    | 2   | 16          | 16       | 0          |
    | 3   | 512         | 512      | 0          |
    | 4   | 65536       | 4096     | 61440      |
    | 5   | 33554432    |          |            |
    | 6   | 68719476736 |          |            |
    +-----+-------------+----------+------------+
    '''

main()
