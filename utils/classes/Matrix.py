from __future__ import annotations

from typing import Callable


class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def __repr__(self):
        return f'{self.x}-{self.y} value: {self.value}'

    def __lt__(self, other):
        return self.value.__lt__(other.value)

    def __le__(self, other):
        return self.value.__le__(other.value)

    def __gt__(self, other):
        return self.value.__gt__(other.value)

    def __ge__(self, other):
        return self.value.__ge__(other.value)

    def __eq__(self, other):
        return self.value.__eq__(other.value)

    def __ne__(self, other):
        return self.value.__ne__(other.value)


class Adjacent:
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    UP_RIGHT = "UR"
    UP_LEFT = "UL"
    DOWN_RIGHT = "DR"
    DOWN_LEFT = "DL"

    def __init__(self, direction, x, y, cell_value):
        self.direction = direction
        self.x = x
        self.y = y
        self.cell_value = cell_value

    def __repr__(self):
        return f"{self.direction} {self.x} {self.y} {self.cell_value}"


class Matrix:

    def __init__(self, height: int, width: int, init_value=None):
        self.matrix = [Matrix.init_row(width, init_value) for _ in range(height)]
        self.height = height
        self.width = width
        self.init_value = init_value

    def get_adjacent(self, x, y, diagonal=False) -> Adjacent:
        adjacent = [Adjacent(Adjacent.UP, x, y - 1, self.get_cell_or_none(x, y - 1)),
                    Adjacent(Adjacent.DOWN, x, y + 1, self.get_cell_or_none(x, y + 1)),
                    Adjacent(Adjacent.LEFT, x - 1, y, self.get_cell_or_none(x - 1, y)),
                    Adjacent(Adjacent.RIGHT, x + 1, y, self.get_cell_or_none(x + 1, y))]

        if diagonal:
            adjacent.append(Adjacent(Adjacent.UP_RIGHT, x + 1, y - 1, self.get_cell_or_none(x + 1, y - 1)))
            adjacent.append(Adjacent(Adjacent.UP_LEFT, x - 1, y - 1, self.get_cell_or_none(x - 1, y - 1)))
            adjacent.append(Adjacent(Adjacent.DOWN_RIGHT, x + 1, y + 1, self.get_cell_or_none(x + 1, y + 1)))
            adjacent.append(Adjacent(Adjacent.DOWN_LEFT, x - 1, y + 1, self.get_cell_or_none(x - 1, y + 1)))

        return adjacent

    def get_row(self, y):
        return self.matrix[y]

    def get_column(self, x):
        return [row[x] for row in self.matrix]

    def get_left(self, x, y):
        return self.get_row(y)[:x]

    def get_right(self, x, y):
        return self.get_row(y)[x+1:]

    def get_top(self, x, y):
        return self.get_column(x)[:y]

    def get_bottom(self, x, y):
        return self.get_column(x)[y+1:]

    def get_sides(self, x: int, y: int):
        """Get in line all sides from current coordinates. Clockwise, starting from right side (R,B,L,T)"""
        return [
            self.get_right(x, y),
            self.get_bottom(x, y),
            self.get_left(x, y),
            self.get_top(x, y),
        ]

    def get_cell(self, x, y):
        return self.matrix[y][x]

    def get_cell_or_none(self, x, y):
        if x >= self.width or x < 0:
            return None
        if y >= self.height or y < 0:
            return None

        return self.matrix[y][x]

    def set_cell(self, x, y, value):
        self.matrix[y][x] = value

    def is_edge(self, x, y):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def map_row(self, y, row_data):
        for i in range(len(row_data)):
            self.matrix[y][i] = row_data[i]

    def __iter__(self):
        self.current_x = 0
        self.current_y = 0
        return self

    def __next__(self):
        if self.current_x >= self.width:
            self.current_x = 0
            self.current_y += 1

        if self.current_y >= self.height:
            raise StopIteration

        item = {
            "cell": self.get_cell(self.current_x, self.current_y),
            "x": self.current_x,
            "y": self.current_y,
        }
        self.current_x += 1

        return item

    def __repr__(self):
        result = ""
        for row in self.matrix:
            for cell in row:
                result += str(cell)
            result += "\n"
        return result

    @staticmethod
    def init_row(size, init_value=None):
        return [init_value for _ in range(size)]

    @staticmethod
    def init_matrix(data, func: Callable = lambda x, y, cell: cell) -> Matrix:
        matrix = Matrix(len(data), len(data[0]))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                matrix.set_cell(x, y, value=func(x, y, cell))

        return matrix
