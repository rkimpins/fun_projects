from board import Grid

def testCollapseRow():
    print("Running tests for collapse_row()")
    grid = Grid(4)
    
    a = [2, 0, 0, 0]
    b = [2, 0, 2, 0]
    c = [2, 2, 2, 0]
    d = [2, 0, 2, 2]
    e = [8, 8, 16, 8]
    f = [2, 0, 2, 4]
    g = [2, 8, 4, 4]
    h = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]

    a_sol = ([2, 0, 0, 0], False)
    b_sol = ([4, 0, 0, 0], True)
    c_sol = ([4, 2, 0, 0], True)
    d_sol = ([4, 2, 0, 0], True)
    e_sol = ([16, 16, 8, 0], True)
    f_sol = ([4, 4, 0, 0], True)
    g_sol = ([2, 8, 8, 0], True)
    h_sol = ([4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], True)

    assert(grid.collapse_row(a) == a_sol)
    assert(grid.collapse_row(b) == b_sol)
    assert(grid.collapse_row(c) == c_sol)
    assert(grid.collapse_row(d) == d_sol)
    assert(grid.collapse_row(e) == e_sol)
    assert(grid.collapse_row(f) == f_sol)
    assert(grid.collapse_row(g) == g_sol)
    assert(grid.collapse_row(h) == h_sol)
"""
def testCollapseLeft():
    print("Running test for collapseLeft()")
    grid = Grid()
    grid._grid = [[0, 0, 0, 0],
                   [0, 0, 0, 4],
                   [2, 0, 2, 16],
                   [2, 4, 4, 2]]
                   
    sol = [[0, 0, 0, 0],
           [4, 0, 0, 0],
           [4, 16, 0, 0],
           [2, 8, 2, 0]]
    
    grid.collapseLeft()
    test = grid._grid
    
    if sol == test:
        print("Left collapse test passed.")
    else:
        print("Test case failed.")


def testCollapseDown():
    print("Running test for collapseDown()")
    grid = Grid()
    grid._grid = [[2, 8, 2, 4],
                   [8, 4, 8, 2],
                   [2, 4, 2, 4],
                   [4, 2, 4, 2]]
                   
    sol = [[2, 0, 2, 4],
           [8, 8, 8, 2],
           [2, 8, 2, 4],
           [4, 2, 4, 2]]
    
    grid.collapseDown()
    test = grid._grid
    
    if sol == test:
        print("Down collapse test passed.")
    else:
        print("Test case failed.")


def testCollapsible():
    print("Running test for collapsible()")
    grid = Grid()
    
    grid.emptiesSet = [0, 1, 2, 3, 4, 5, 6, 8]
    grid._grid = [[0, 0, 0, 0],
                   [0, 0, 0, 4],
                   [2, 0, 2, 16],
                   [2, 4, 4, 2]]

    if grid.collapsible():
        print('Test (a) passed.')
    else:
        print('Test (a) failed.')

    grid.emptiesSet = []
    grid._grid = [[2, 8, 2, 4],
                   [4, 4, 8, 2],
                   [2, 8, 2, 4],
                   [4, 2, 4, 2]]

    if grid.collapsible():
        print('Test (b) passed.')
    else:
        print('Test (b) failed.')

    grid.emptiesSet = []
    grid._grid = [[2, 8, 2, 4],
                   [8, 4, 8, 2],
                   [2, 4, 2, 4],
                   [4, 2, 4, 2]]

    if grid.collapsible():
        print('Test (c) passed.')
    else:
        print('Test (c) failed.')
    
    grid.emptiesSet = []
    grid._grid = [[2, 4, 2, 4],
                   [4, 2, 4, 2],
                   [2, 4, 2, 4],
                   [4, 2, 4, 2]]

    if not grid.collapsible():
        print('Test (d) passed.')
    else:
        print('Test (d) failed.')


def testEmpties():
    print("Running test for updateEmptiesSet()")
    grid = Grid()
    grid._grid = [[0, 0, 0, 0],
                  [0, 0, 0, 4],
                  [2, 0, 2, 16],
                  [2, 4, 4, 0]]
    grid.updateEmptiesSet()
    truth = [0, 1, 2, 3, 4, 5, 6, 9, 15]
    if grid.emptiesSet == truth:
        print('Empties set test passed.')
    else:
        print('Empties set test failed.')

def testRollout():
    pass
    #x = Grid()
    #y = x.copy()
    #x.drawGrid()
    #y.drawGrid()
    #x = Grid(4)
    #print(x.collapse_row([0, 0, 2, 2]))
    #x.spawn_tile()
    #x.show()
    #print()
    #x.play_move(UP)
    #x.show()
    #print()
    #x.play_move(RIGHT)
    #x.show()
    #print()
    #x.play_move(DOWN)
    #x.show()
    #print()
    #x.play_move(LEFT)
    #x.show()
    #print()


# Uncomment the tests for the function you want to check

#testCollapseRow()
#testCollapseLeft()
#testCollapseDown()
#testCollapsible()
#testEmpties()

"""