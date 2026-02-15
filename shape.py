import random
from cell import Cell

## shapes will ha
class Shape:
    matrix: list[list[Cell]]
    color: Cell
    name: str
    ## coordinates of the top left corner of the shape in the game grid
    x: int
    y: int

    SHAPES = {
        'I': [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'J': [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'L': [
            [0, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'O': [
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'S': [
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'T': [
            [0, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        'Z': [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    }

    def __init__(self, shapeMatrix: list[list[Cell]], x: int, y: int, color: Cell, name: str):
        self.matrix = shapeMatrix
        self.x = x
        self.y = y
        self.color = color
        self.name = name

    @staticmethod
    def generateRandomShape(self, x:int, y:int):
        self.x = x
        self.y = y
        randomColor = random.choice([Cell.Red, Cell.Blue, Cell.Green, Cell.Yellow, Cell.Purple])
        self.color = randomColor
        self.name = random.choice(list(self.SHAPES.keys()))
        temp = self.SHAPES[self.name]
        self.matrix = [[Cell.Empty if temp[i][j] == 0 else randomColor for j in range(len(temp[0]))] for i in range(len(temp))]
        return self

    