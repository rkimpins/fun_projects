import random as rnd
import os
import sys

class Grid():
    def __init__(self, row=4, col=4, initial=2):
        self.row = row                              # number of rows in grid
        self.col = col                              # number of columns in grid
        self.initial = initial                      # number of initial cells filled
        self.score = 0
        
        self._grid = self.createGrid(row, col)    # creates the grid specified above

        self.emptiesSet = list(range(row * col))    # list of empty cells
                 
        for _ in range(self.initial):               # assignation to two random cells
            self.assignRandCell(init=True)


    def createGrid(self, row, col):
        # creates a blank grid, consisting of 0's
        # structure is a list of lists
        grid = []
        for index in range(row):
            grid.append([0]*col)
        return grid
    
    
    def setCell(self, cell, val):
        # Changes the value in the cell to the value
        col, row = divmod(cell, self.col)
        self._grid[col][row] = val
        

    def getCell(self, cell):
        # Acesses the value of a cell in the grid
        # Numbers go from 0-15, left to right, top to bottem
        col, row = divmod(cell, self.col)
        return self._grid[col][row]
        

    def assignRandCell(self, init=False):
    
        """
        This function assigns a random empty cell of the grid 
        a value of 2 or 4.
        
        In __init__() it only assigns cells the value of 2.
        
        The distribution is set so that 75% of the time the random cell is
        assigned a value of 2 and 25% of the time a random cell is assigned 
        a value of 4
        """
        
        if len(self.emptiesSet):
            cell = rnd.sample(self.emptiesSet, 1)[0]
            if init:
                self.setCell(cell, 2)
            else:
                cdf = rnd.random()
                if cdf > 0.75:
                    self.setCell(cell, 4)
                else:
                    self.setCell(cell, 2)
            self.emptiesSet.remove(cell)


    def drawGrid(self):
    
        """
        This function draws the grid representing the state of the game
        grid
        """
        
        for i in range(self.row):
            line = '\t|'
            for j in range(self.col):
                if not self.getCell((i * self.row) + j):
                    line += ' '.center(5) + '|'
                else:
                    line += str(self.getCell((i * self.row) + j)).center(5) + '|'
            print(line)
        print()
    
    
    def updateEmptiesSet(self):
        # Updates the emptiesSet, which is a list of all the empty squares in the grid 
        self.emptiesSet = []
        for index in range(self.col*self.row):
            if self.getCell(index) == 0:
                self.emptiesSet.append(index)
                
    
    def collapsible(self):
        # returns a boolean representing whether the grid is collapsable or not
        gridList = []
        for index in range(self.col*self.row):
            gridList.append(self.getCell(index))
        if 0 in gridList:
            return True
        for index in range(len(gridList)):
            if index/self.row not in range(self.row):
                if gridList[index-1] == gridList[index]:
                    return True
            if index not in range(self.col):
                if gridList[index-self.col] == gridList[index]:
                    return True
        return False
        
        
    def addScore(self, list1, list2):
        # Takes the initial state(list1) and final state(list2) of a move
        # and caculates and adds the score to the self.score attribute
        # according to the rules of 2048
        # Does not alter the lists it is provided with
        list1 = [x for x in list1 if x != 0]
        list2 = [x for x in list2 if x != 0]
        list2.sort(reverse=True)
        counter = len(list1) - len(list2)
        while counter != 0:
            
            if list2[0] in list1:
                list1.remove(list2[0])
                list2.pop(0)
            elif list2[0]/2 in list1:
                for _ in range(2):
                    list1.remove(list2[0]/2)
                self.score += list2[0]
                list2.pop(0)
                counter -= 1      
            
    def collapseRow(self, lst):
        # This function takes a list of integers, and collapses it to the left
        # according to the rules of 2048
        # Returns the collapsed list, and a boolean of whether the list was collapsed
        # Also Updates the score counter according to the rules of 2048
        originalLst = list(lst)
        collapsed = False
        if 0 in lst:
            for index in range(lst.index(0), len(lst)):
                if lst[index]!=0:
                    collapsed = True
        
        if 0 in lst:
            for index in range(len(lst)-1):
                lst.append(lst.pop(lst.index(0)))
        
        for index in range(1,len(lst)):
            if lst[index]!=0:
                if lst[index-1]==lst[index]:
                    lst[index-1]*=2
                    lst[index]=0
                    collapsed = True
        
        if 0 in lst:
            for index in range(len(lst)-1):
                lst.append(lst.pop(lst.index(0)))
        
        self.addScore(originalLst, lst)
        return lst, collapsed
    

    def collapseLeft(self):
        # Collapsed the grid to the left
        # Uses only get and set to retrieve and edit values from the grid
        # Which is a very frustrating way to have to do it, especially when keeping
        # the grid as a lists of lists allows simpler solution
        # Edits the grid, and returns true if any of the rows were collapsed
        collapsedList = []
        for indexRow in range(self.row):
            row=[]
            for indexCol in range(self.col):
                row.append(self.getCell(indexCol + indexRow*self.col))
            row, collapsed = self.collapseRow(row)
            collapsedList.append(collapsed)
            for index in range(self.col):
                self.setCell(index + indexRow*self.col, row[index]) 
        return any(collapsedList)


    def collapseRight(self):
        # Collapses the grid to the right
        # Exactly the same as collapseLeft, but reverses the values
        # Edits the grid, and returns true if any of the rows were collapsed
        
        collapsedList = []
        for indexRow in range(self.row):
            row=[]
            for indexCol in range(self.col):
                row.append(self.getCell(indexCol + indexRow*self.col))
            row.reverse()
            row, collapsed = self.collapseRow(row)
            collapsedList.append(collapsed)
            row.reverse()
            for index in range(self.col):
                self.setCell(index + indexRow*self.col, row[index]) 
        return any(collapsedList)


    def collapseUp(self):
        # Collapses the grid up
        # Edits the grid, returns true if any of the columns were collapsed
        collapsedList = []
        for indexRow in range(self.row):
            col = []
            for indexCol in range(self.col):
                col.append(self.getCell(indexCol*self.row + indexRow))
            col, collapsed = self.collapseRow(col)
            collapsedList.append(collapsed)
            for index in range(self.row):
                self.setCell(index*self.row + indexRow, col[index]) 
        return any(collapsedList)



    def collapseDown(self):
        # Collapses teh grid down
        # Edits the grid, returns true if any of the columns were collapsed
        collapsedList = []
        for indexRow in range(self.row):
            col = []
            for indexCol in range(self.col):
                col.append(self.getCell(indexCol*self.row + indexRow))
            col.reverse()
            col, collapsed = self.collapseRow(col)
            collapsedList.append(collapsed)
            col.reverse()
            for index in range(self.row):
                self.setCell(index*self.row + indexRow, col[index]) 
        return any(collapsedList)        
        

class Game():
    def __init__(self, row=4, col=4, initial=2):
    
        """
        Creates a game grid and begins the game
        """
        
        self.game = Grid(row, col, initial)
        self.play()
    
    
    def printPrompt(self):
        
        """
        Prints the instructions and the game grid with a move prompt
        """
    
        if sys.platform == 'win32':
            os.system("cls")
        else:
            os.system("clear")
        
        print('Press "w", "a", "s", or "d" to move Up, Left, Down or Right respectively.')
        print('Enter "p" to quit.\n')
        self.game.drawGrid()
        print('\nScore: ' + str(self.game.score))


    def play(self):
    
        moves = {'w' : 'Up',
                 'a' : 'Left',
                 's' : 'Down',
                 'd' : 'Right'}
        
        stop = False
        collapsible = True
        
        while not stop and collapsible:
            self.printPrompt()
            key = input('\nEnter a move: ')
            
            while not key in list(moves.keys()) + ['p']:
                self.printPrompt()
                key = input('\nEnter a move: ')

            if key == 'p':
                stop = True
            else:
                move = getattr(self.game, 'collapse' + moves[key])
                collapsed = move()
                
                if collapsed:
                    self.game.updateEmptiesSet()
                    self.game.assignRandCell()
                    
                collapsible = self.game.collapsible()
                 
        if not collapsible:
            if sys.platform == 'win32':
                os.system("cls")
            else:
                os.system("clear")
            print()
            self.game.drawGrid()
            print('\nScore: ' + str(self.game.score))
            print('No more legal moves.')


def main():
    game = Game()
    
main()
