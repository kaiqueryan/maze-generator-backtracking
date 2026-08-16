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
        self.stop = False

    def generateMaze(self):

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

        while self.stop != 'y':
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

        self.stop = input('Stop? (y/n): ')


    def moveRight(self):

        row, column = self.actualCell
        actionCell = (row, column + 1)

        if actionCell in self.visitedCells:
            print('Cell already visited.')
            return

        if column + 1 >= self.mazeSize:
            print('Cannot move right, out of bounds.')
            return

        y1 = row * self.cellSize + self.wallSize
        x1 = column * self.cellSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize + self.wallSize

        self.maze[y1 : y2, x2 - self.wallSize : x2] = 255

        self.actualCell = (row, column + 1)  
        self.visitedCells.append(self.actualCell)


    def moveLeft(self):

        row, column = self.actualCell
        actionCell = (row, column - 1)

        if actionCell in self.visitedCells:
            print('Cell already visited.')
            return

        if column == 0:
            print('Cannot move left, already at the leftmost column.')
            return

        y1 = row * self.cellSize + self.wallSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y1 : y2, x1 - self.wallSize: x2] = 255

        self.actualCell = (row, column - 1)  
        self.visitedCells.append(self.actualCell)


    def moveDown(self):

        row, column = self.actualCell
        actionCell = (row + 1, column)

        if actionCell in self.visitedCells:
            print('Cell already visited.')
            return

        if row + 1 >= self.mazeSize:
            print('Cannot move down, out of bounds.')
            return

        y1 = row * self.cellSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y2 : y2 + self.wallSize, x1 : x2] = 255

        self.actualCell = (row + 1, column)  
        self.visitedCells.append(self.actualCell)

    def moveUp(self):

        row, column = self.actualCell
        actionCell = (row - 1, column)

        if actionCell in self.visitedCells:
            print('Cell already visited.')
            return

        if row == 0:
            print('Cannot move up, already at the top row.')
            return

        y1 = row * self.cellSize
        x1 = column * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x2 = (column + 1) * self.cellSize

        self.maze[y1 : y1 + self.wallSize, x1 : x2] = 255

        self.actualCell = (row - 1, column)  
        self.visitedCells.append(self.actualCell)  
   

maze = BacktrackingMaze(10)
maze.generateMaze()