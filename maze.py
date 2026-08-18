import numpy as np
import random
import cv2 as opencv 

class BacktrackingMaze:

    def __init__(self, mazeSize):
        self.mazeSize = mazeSize
        self.cellSize = 40
        self.wallSize = 6
        self.visitedCells = []
        self.actualCell = (0, 0)
        self.image_dimension = (self.mazeSize * self.cellSize) + self.wallSize
        self.maze  = np.zeros((self.image_dimension, self.image_dimension), dtype=np.uint8)
        self.blockedMoves = []
        self.mazeCellsQuantity = self.mazeSize * self.mazeSize
        self.cellsToVisit = []

    def generateMaze(self):

        self.generateMazeCellsToVisit(self.mazeSize)

        for row in range(self.mazeSize):
            for column in range(self.mazeSize):
                y1 = row * self.cellSize + self.wallSize 
                x1 = column * self.cellSize + self.wallSize 
                y2 = (row + 1) * self.cellSize 
                x2 = (column + 1) * self.cellSize  

                self.maze[y1:y2, x1:x2] = 255

        startPointX1 = 0 * self.cellSize + self.wallSize
        startPointX2 = 1 * self.cellSize
        startPointY1 = 0 * self.cellSize + self.wallSize

        endPointX1 = (self.mazeSize - 1) * self.cellSize + self.wallSize
        endPointX2 = self.mazeSize * self.cellSize
        endPointY1 = self.mazeSize * self.cellSize
        endPointY2 = self.mazeSize * self.cellSize + self.wallSize

        # Create the entrance and exit of the maze

        self.maze[startPointY1 - self.wallSize : startPointY1, startPointX1 : startPointX2] = 255
        self.maze[endPointY1 : endPointY2, endPointX1 : endPointX2] = 255

        while self.cellsToVisit:

            print('Actual Cell:', self.actualCell)
            print('Visited cells:', len(self.visitedCells))
            print('Cells to visit:', len(self.cellsToVisit))

            self.chooseAction()
        
        opencv.imshow("Maze", self.maze)
        opencv.waitKey(0) 
        opencv.destroyAllWindows()


    def chooseAction(self):  

        actions = [
            'up',
            'down',
            'left',
            'right'
        ]

        randomAction = random.choice(actions)
        print('randomAction:', randomAction) 
         
        if randomAction == 'down':
            self.moveDown() 

        if randomAction == 'up':
            self.moveUp()

        if randomAction == 'left':
            self.moveLeft()

        if randomAction == 'right':
            self.moveRight()


    def moveRight(self):

        row, column = self.actualCell
        actionCell = (row, column + 1)

        if self.verifyCellBlocked():
            return 

        if 'right' in self.blockedMoves:
            print('Move right is blocked.')
            return

        if actionCell not in self.cellsToVisit:
            self.blockedMoves.append('right')
            print('Cell already visited.')
            return

        if column + 1 >= self.mazeSize:
            self.blockedMoves.append('right')
            print('Cannot move right, out of bounds.')
            return

        y1 = row * self.cellSize + self.wallSize
        x1 = column * self.cellSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize + self.wallSize

        self.maze[y1 : y2, x2 - self.wallSize : x2] = 255

        self.actualCell = (row, column + 1)
        self.blockedMoves = []  

        self.controlCells()


    def moveLeft(self):

        row, column = self.actualCell
        actionCell = (row, column - 1)

        if self.verifyCellBlocked():
            return 

        if 'left' in self.blockedMoves:
            print('Move left is blocked.')
            return

        if actionCell not in self.cellsToVisit:
            self.blockedMoves.append('left')
            print('Cell already visited.')
            return

        if column == 0:
            self.blockedMoves.append('left')
            print('Cannot move left, already at the leftmost column.')
            return

        y1 = row * self.cellSize + self.wallSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y1 : y2, x1 - self.wallSize: x2] = 255

        self.actualCell = (row, column - 1)  
        self.blockedMoves = []

        self.controlCells()


    def moveDown(self):

        row, column = self.actualCell
        actionCell = (row + 1, column)

        if self.verifyCellBlocked():
            return

        if 'down' in self.blockedMoves:
            print('Move down is blocked.')
            return

        if actionCell not in self.cellsToVisit:
            self.blockedMoves.append('down')
            print('Cell already visited.')
            return

        if row + 1 >= self.mazeSize:
            self.blockedMoves.append('down')
            print('Cannot move down, out of bounds.')
            return

        y1 = row * self.cellSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y2 : y2 + self.wallSize, x1 : x2] = 255

        self.actualCell = (row + 1, column)  
        self.blockedMoves = []

        self.controlCells()

    def moveUp(self):

        row, column = self.actualCell
        actionCell = (row - 1, column)

        if self.verifyCellBlocked():
            return

        if 'up' in self.blockedMoves:
            print('Move up is blocked.')
            return

        if actionCell not in self.cellsToVisit:
            self.blockedMoves.append('up')
            print('Cell already visited.')
            return

        if row == 0:
            self.blockedMoves.append('up')
            print('Cannot move up, already at the top row.')
            return

        y1 = row * self.cellSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y1 : y1 + self.wallSize, x1 : x2] = 255

        self.actualCell = (row - 1, column)  
        self.blockedMoves = []

        self.controlCells()


    def verifyCellBlocked(self):

        print('Blocked moves:', self.blockedMoves)

        if 'up' in self.blockedMoves and 'down' in self.blockedMoves and 'left' in self.blockedMoves and 'right' in self.blockedMoves:

            print('All moves are blocked. Backtracking to previous cell.')

            self.visitedCells.pop()  # Remove the last visited cell
            self.actualCell = self.visitedCells[-1]
            self.blockedMoves = []

            return True

        
        return False


    def generateMazeCellsToVisit(self, mazeSize):

        mazeCellsToVisit = []
        for row in range(mazeSize):
            for column in range(mazeSize):
                mazeCellsToVisit.append((row, column))

        self.cellsToVisit = mazeCellsToVisit
       

    def controlCells(self):

        if self.actualCell in self.cellsToVisit:
            self.cellsToVisit.remove(self.actualCell)
        
        if self.actualCell not in self.visitedCells:
            self.visitedCells.append(self.actualCell)  
        


maze = BacktrackingMaze(20)
maze.generateMaze()