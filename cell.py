from enum import Enum

class Cell(Enum):
    Empty = 0
    Red = 1
    Blue = 2
    Green = 3
    Yellow = 4
    Purple = 5

    @staticmethod
    def getColorValue(self):
        if self == Cell.Empty:
            return (255, 255, 255)
        elif self == Cell.Red:
            return (255, 0, 0)
        elif self == Cell.Blue:
            return (0, 0, 255)
        elif self == Cell.Green:
            return (0, 255, 0)
        elif self == Cell.Yellow:
            return (125, 125, 0)
        elif self == Cell.Purple:
            return (255, 0, 255)