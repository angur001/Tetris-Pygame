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
        self.gameSpeed = 250
        self.addRandomShape()

    def getGameSpeed(self):
        return self.gameSpeed
        
    def addRandomShape(self):
        newShape = Shape.generateRandomShape(self.WIDTH // 2, 0)
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
                if self.currentShape.matrix[i][j] != Cell.Empty:
                    self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] = Cell.Empty

    def step(self):
        if self.currentShape:
            if self.canMoveDown():
                self.removeShadow()
                self.currentShape.y += 1
                self.updateGameGrid()
            else:
                self.addRandomShape()
    
    def canMoveDown(self):
        for j in range(len(self.currentShape.matrix[0])):
            for i in range(len(self.currentShape.matrix) - 1, -1, -1):
                if self.currentShape.matrix[i][j] != Cell.Empty:
                    if self.currentShape.y + i + 1 >= self.HEIGHT or self.gameGrid[self.currentShape.y + i + 1][self.currentShape.x + j] != Cell.Empty:
                        return False
                    break
        return True

    def canMoveLeft(self):
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])):
                if self.currentShape.matrix[i][j] != Cell.Empty:
                    if self.currentShape.x + j - 1 < 0 or self.gameGrid[self.currentShape.y + i][self.currentShape.x + j - 1] != Cell.Empty:
                        return False
                    break
        return True

    def canMoveRight(self):
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])-1,-1,-1):
                if self.currentShape.matrix[i][j] != Cell.Empty:
                    if self.currentShape.x + j + 1 >= self.WIDTH or self.gameGrid[self.currentShape.y + i][self.currentShape.x + j + 1] != Cell.Empty:
                        return False
                    break
        return True

    def canRotate(self):
        rotated_shape = self.currentShape.peekAtNextRotation()
        curr = self.currentShape
        for i in range(len(rotated_shape.matrix)):
            for j in range(len(rotated_shape.matrix[0])):
                if rotated_shape.matrix[i][j] == Cell.Empty:
                    continue
                gy, gx = rotated_shape.y + i, rotated_shape.x + j
                if gy < 0 or gy >= self.HEIGHT or gx < 0 or gx >= self.WIDTH:
                    return False
                if self.gameGrid[gy][gx] == Cell.Empty:
                    continue
                ci, cj = gy - curr.y, gx - curr.x
                if 0 <= ci < len(curr.matrix) and 0 <= cj < len(curr.matrix[0]) and curr.matrix[ci][cj] != Cell.Empty:
                    continue
                return False
        return True

    def tryMoveLeft(self):
        if self.currentShape:
            if self.canMoveLeft():
                self.removeShadow()
                self.currentShape.x -= 1
                self.updateGameGrid()
    
    def tryMoveRight(self):
        if self.currentShape:
            if self.canMoveRight():
                self.removeShadow()
                self.currentShape.x += 1
                self.updateGameGrid()

    def tryRotate(self):
        if self.currentShape:
            if self.canRotate():
                self.removeShadow()
                self.currentShape.rotate()
                self.updateGameGrid()
    
