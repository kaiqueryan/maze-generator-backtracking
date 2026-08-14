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

        while self.actualCell != (400, 400) and self.stop != 'y':
            self.chooseAction()
        
        opencv.imshow("Maze", self.maze)
        opencv.waitKey(0) 
        opencv.destroyAllWindows()


    def chooseAction(self):  

        row, column = self.actualCell

        print('actualCell:', self.actualCell)

        actions = {
            'up': (row - 1, column), 
            'down': (row + 1, column),  
            'left': (row, column - 1),
            'right': (row, column + 1)
        }

        randomAction = random.choice(list(actions.keys()))
        print('randomAction:', randomAction) 

        if randomAction == 'up' and self.actualCell[0] <= 4: 
            print('Action not valid:', randomAction)
            return

        if randomAction == 'left' and self.actualCell[1] < 40:
            print('Action not valid:', randomAction)
            return

        if randomAction == 'right' and self.actualCell[1] >= 90:
            print('Action not valid:', randomAction)
            return
        
        if randomAction == 'down' and self.actualCell[0] >= 366:
            print('Action not valid:', randomAction)
            return
         
        if randomAction == 'down':
            self.moveDown(actions[randomAction]) 

        if randomAction == 'up':
            self.moveUp(actions[randomAction])

        if randomAction == 'left':
            self.moveLeft(actions[randomAction])

        if randomAction == 'right':
            self.moveRight(actions[randomAction])

        self.stop = input('Stop? (y/n): ')


    def moveDown(self, action): 

        if not self.isValidAction(action):
            print('Action not valid:', action)
            return

        row, column = self.actualCell 
      
        y2 = action[0] * self.cellSize
        x1 = column * self.cellSize + self.wallSize
        x2 = (column + 1) * self.cellSize

        self.maze[y2 : y2 + self.wallSize, x1 : x2] = 255  

        self.visitedCells.append(action)

    
    def moveUp(self, action):

        if not self.isValidAction(action):
            print('Action not valid:', action)
            return

        row, column = self.actualCell 

        y1 = action[0] * self.cellSize + self.wallSize
        x1 = column * self.cellSize + self.wallSize
        x2 = (column + 1) * self.cellSize

        self.maze[y1 - self.wallSize : y1, x1 : x2] = 255  

        self.visitedCells.append(action)
        

    def moveLeft(self, action):

        if not self.isValidAction(action):
            print('Action not valid:', action)
            return

        row, column = self.actualCell 

        y1 = row * self.cellSize + self.wallSize 
        y2 = (row + 1) * self.cellSize
        x1 = action[1] * self.cellSize

        self.maze[y1 : y2, x1 : x1 + self.wallSize] = 255  

        self.visitedCells.append(action)
        

    def moveRight(self, action):  

        if not self.isValidAction(action):
            print('Action not valid:', action)
            return

        row, column = self.actualCell 

        y1 = row * self.cellSize + self.wallSize
        y2 = (row + 1) * self.cellSize
        x1 = action[1] * self.cellSize

        self.maze[y1 : y2, x1 : x1 + self.wallSize] = 255  

        self.visitedCells.append(action)


    def isValidAction(self, action):

        row, column = action 

        if action not in self.visitedCells:
            self.actualCell = action
            return True
        else:
            return False
    

maze = BacktrackingMaze(10)
maze.generateMaze()