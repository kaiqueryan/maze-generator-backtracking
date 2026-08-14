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
        self.maze = maze = np.zeros((self.image_dimension, self.image_dimension), dtype=np.uint8)

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

        self.chooseAction(self.actualCell)

        opencv.imshow("Maze", self.maze)
        opencv.waitKey(0)
        opencv.destroyAllWindows()


    def chooseAction(self, currentCell):

        row, column = currentCell 

        actions = {
            'up': (row - 1, column),
            'down': (row + 1, column),
            'left': (row, column - 1),
            'right': (row, column + 1)
        }

        randomAction = random.choice(list(actions.keys()))

        if randomAction == 'up' and row == 0:
            print('Action not valid:', randomAction)
            self.chooseAction(self.actualCell)

        print('Random Action:', randomAction)
        self.isValidAction(actions[randomAction], currentCell)


    def isValidAction(self, action, currentCell):

        row, column = currentCell
        newRow, newColumn = action

        if 0 <= newRow < self.mazeSize and 0 <= newColumn < self.mazeSize:
            if (newRow, newColumn) not in self.visitedCells:

                print('Valid Action:', action)
                self.visitedCells.append((newRow, newColumn))
                self.actualCell = (newRow, newColumn)
                self.removeWall(currentCell, action)
                self.chooseAction(self.actualCell)

            else:
                print('Action already visited:', action)
                self.chooseAction(self.actualCell)


    def removeWall(self, currentCell, action):

        row, column = currentCell
        newRow, newColumn = action

       


       


maze = BacktrackingMaze(10)
maze.generateMaze()