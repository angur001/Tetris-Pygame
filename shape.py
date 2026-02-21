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
    rotation_index: int

    SHAPES = {
        'I': [
            [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]],
            [[0, 0, 0, 0], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]],
            [[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]
        ],
        'J': [
            [[1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 1, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0]]
        ],
        'L': [
            [[0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [1, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0]],
            [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        ],
        'O': [
            [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        ],
        'S': [
            [[0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0]],
            [[1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        ],
        'T': [
            [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        ],
        'Z': [
            [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 1, 0], [0, 1, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
            [[0, 0, 0, 0], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]],
            [[0, 1, 0, 0], [1, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]
        ]
    }

    def __init__(self, shapeMatrix: list[list[Cell]], x: int, y: int, color: Cell, name: str):
        self.matrix = shapeMatrix
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.rotation_index = 0

    def mapRawMatrixToColor(self, matrix: list[list[Cell]]):
        return [[Cell.Empty if matrix[i][j] == 0 else self.color for j in range(len(matrix[0]))] for i in range(len(matrix))]

    def peekAtNextRotation(self):
        next_rotation_index = (self.rotation_index + 1) % 4
        temp = Shape.SHAPES[self.name][next_rotation_index]
        return Shape(self.mapRawMatrixToColor(temp), self.x, self.y, self.color, self.name)
    
    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % 4
        temp = Shape.SHAPES[self.name][self.rotation_index]
        self.matrix = self.mapRawMatrixToColor(temp)

    @staticmethod
    def generateRandomShape(x: int, y: int):
        name = random.choice(list(Shape.SHAPES.keys()))
        color = random.choice([Cell.Red, Cell.Blue, Cell.Green, Cell.Yellow, Cell.Purple])
        raw = Shape.SHAPES[name][0]
        matrix = [[Cell.Empty if raw[i][j] == 0 else color for j in range(len(raw[0]))] for i in range(len(raw))]
        return Shape(matrix, x, y, color, name)


    