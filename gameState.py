from ast import Return
from nt import isatty
import pygame
from cell import Cell
from shape import Shape
import time
from displays import Displays

class GameState:

    gameGrid: list[list[Cell]]
    score: int
    gameSpeed: int
    currentShape: Shape
    nextShape: Shape

    HEIGHT = 20
    WIDTH = 10


    def __init__(self):
        self.gameGrid = [[Cell.Empty for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        self.score = 0
        self.gameSpeed = 250
        self.currentShape = None
        self.addRandomShape()

    def getGameSpeed(self):
        return self.gameSpeed
        
    def addRandomShape(self):
        if not self.currentShape:
            self.currentShape = Shape.generateRandomShape(self.WIDTH // 2 - 1, -4)
            self.nextShape = Shape.generateRandomShape(self.WIDTH // 2 - 1, -4)
            self.updateGameGrid()
        else:
            self.currentShape = self.nextShape
            self.nextShape = Shape.generateRandomShape(self.WIDTH // 2 - 1, -4)
            self.updateGameGrid()

    def updateGameGrid(self):
        # move down current shape on the game grid (to be isolated later in another function)
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])):
                if self.currentShape.matrix[i][j] != Cell.Empty and self.currentShape.y + i >= 0:
                    self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] = self.currentShape.matrix[i][j]
        # check for lines and remove them
        self.checkForLines()

    def removeShadow(self):
        for i in range(len(self.currentShape.matrix)):
            for j in range(len(self.currentShape.matrix[0])):
                if self.currentShape.matrix[i][j] != Cell.Empty and self.currentShape.y + i >= 0:
                    self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] = Cell.Empty
    
    def step(self):
        if self.gameOver():
            return
        if self.currentShape:
            if self.canMoveDown():
                self.removeShadow()
                self.currentShape.y += 1
                self.updateGameGrid()
            else:
                self.addRandomShape()

    def checkForLines(self):
        # Find all full lines in the grid
        full_rows = [
            i
            for i in range(self.HEIGHT)
            if all(self.gameGrid[i][j] != Cell.Empty for j in range(self.WIDTH))
        ]

        # Nothing to clear
        if not full_rows:
            return

        full_rows_set = set(full_rows)

        # Start from the bottom and move non-full rows down, effectively
        # sliding the blocks downward over the cleared lines.
        write_row = self.HEIGHT - 1
        for i in range(self.HEIGHT - 1, -1, -1):
            if i in full_rows_set:
                # This row is cleared; skip copying it
                continue

            if write_row != i:
                for j in range(self.WIDTH):
                    self.gameGrid[write_row][j] = self.gameGrid[i][j]
            write_row -= 1

        # Any remaining rows above the last written row become empty,
        # matching the number of cleared lines.
        for i in range(write_row, -1, -1):
            for j in range(self.WIDTH):
                self.gameGrid[i][j] = Cell.Empty



    def canMoveDown(self):
        for j in range(len(self.currentShape.matrix[0])):
            for i in range(len(self.currentShape.matrix) - 1, -1, -1):
                if self.currentShape.matrix[i][j] != Cell.Empty and self.currentShape.y + i >= 0:
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
    
        return False
   
    def gameOver(self):
        if not self.canMoveDown():
            for i in range(len(self.currentShape.matrix)):
                for j in range(len(self.currentShape.matrix[0])):
                        if self.currentShape.matrix[i][j] != Cell.Empty and self.currentShape.y + i < 0:
                            if self.gameGrid[self.currentShape.y + i][self.currentShape.x + j] != Cell.Empty:
                                return True
        return False
    
