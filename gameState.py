from cell import Cell
from shape import Shape


class GameState:

    gameGrid: list[list[Cell]]
    score: int
    gameSpeed: int
    currentShape: Shape

    HEIGHT = 20
    WIDTH = 10


    def __init__(self):
        self.gameGrid = [[Cell.Empty for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.score = 0
        self.gameSpeed = 1000 ## i will use this to control difficulty later
        self.addRandomShape()

    def getGameSpeed(self):
        return self.gameSpeed
        
    def addRandomShape(self):
        newShape = Shape.generateRandomShape(Shape, self.WIDTH // 2, 0)
        self.currentShape = newShape
        self.updateGameGrid()

    def updateGameGrid(self):
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])):
                if self.currentShape.matrix[i][j] != Cell.Empty:
                    self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] = self.currentShape.matrix[i][j]

    def removeShadow(self):
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])):
                if self.currentShape.y + i < self.HEIGHT or self.currentShape.x + j < self.WIDTH:
                    self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] = Cell.Empty

    def step(self):
        if self.currentShape:
            self.removeShadow()
            # if self.checkCollision():
            self.currentShape.y += 1
            self.updateGameGrid()
