from __future__ import annotations

from typing import Callable, Any, Type


class Direction:
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"
    UP_RIGHT = "UR"
    UP_LEFT = "UL"
    DOWN_RIGHT = "DR"
    DOWN_LEFT = "DL"


class Cell:
    def __init__(self, x: int, y: int, value: Any, matrix: Matrix | Type[Matrix]):
        self.x = x
        self.y = y
        self.value = value
        self.matrix = matrix

    def is_edge(self) -> bool:
        return self.matrix.is_edge(self.x, self.y)

    def get_sides(self) -> list[list[Cell | Type[Cell]]]:
        """Get in line all sides from current coordinates. Clockwise, starting from right side (R,B,L,T)"""
        return self.matrix.get_sides(self.x, self.y)

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


class Matrix:

    def __init__(self, height: int, width: int, init_value: Any = None):
        self.matrix = [[Cell(x, y, init_value, self) for x in range(width)] for y in range(height)]
        self.height = height
        self.width = width
        self.init_value = init_value

    def get_adjacent(self, x: int, y: int, diagonal: bool = False) -> dict[str, Cell | Type[Cell]]:
        adjacent = {
            Direction.UP: self.get_cell_or_none(x, y - 1),
            Direction.DOWN: self.get_cell_or_none(x, y + 1),
            Direction.LEFT: self.get_cell_or_none(x - 1, y),
            Direction.RIGHT: self.get_cell_or_none(x + 1, y),
        }

        if diagonal:
            adjacent[Direction.UP_RIGHT] = self.get_cell_or_none(x + 1, y - 1)
            adjacent[Direction.UP_LEFT] = self.get_cell_or_none(x - 1, y - 1)
            adjacent[Direction.DOWN_RIGHT] = self.get_cell_or_none(x + 1, y + 1)
            adjacent[Direction.DOWN_LEFT] = self.get_cell_or_none(x - 1, y + 1)

        return adjacent

    def get_row(self, y: int) -> list[Cell | Type[Cell]]:
        return self.matrix[y]

    def get_column(self, x: int) -> list[Cell | Type[Cell]]:
        return [row[x] for row in self.matrix]

    def get_left(self, x: int, y: int) -> list[Cell | Type[Cell]]:
        return self.get_row(y)[:x]

    def get_right(self, x: int, y: int) -> list[Cell | Type[Cell]]:
        return self.get_row(y)[x + 1:]

    def get_top(self, x: int, y: int) -> list[Cell | Type[Cell]]:
        return self.get_column(x)[:y]

    def get_bottom(self, x: int, y: int) -> list[Cell | Type[Cell]]:
        return self.get_column(x)[y + 1:]

    def get_sides(self, x: int, y: int) -> list[list[Cell | Type[Cell]]]:
        """Get in line all sides from current coordinates. Clockwise, starting from right side (R,B,L,T)"""
        return [
            self.get_right(x, y),
            self.get_bottom(x, y),
            self.get_left(x, y),
            self.get_top(x, y),
        ]

    def get_cell(self, x: int, y: int) -> Cell | Type[Cell]:
        return self.matrix[y][x]

    def set_cell(self, x: int, y: int, cell: Cell | Type[Cell]):
        self.matrix[y][x] = cell

    def get_cell_or_none(self, x: int, y: int) -> Cell | Type[Cell] | None:
        if x >= self.width or x < 0:
            return None
        if y >= self.height or y < 0:
            return None

        return self.matrix[y][x]

    def is_edge(self, x: int, y: int):
        return x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1

    def __iter__(self):
        self.current_x = 0
        self.current_y = 0
        return self

    def __next__(self) -> Cell | Type[Cell]:
        if self.current_x >= self.width:
            self.current_x = 0
            self.current_y += 1

        if self.current_y >= self.height:
            raise StopIteration

        cell = self.get_cell(self.current_x, self.current_y)
        self.current_x += 1

        return cell

    def __repr__(self):
        result = ""
        for row in self.matrix:
            for cell in row:
                result += str(cell.value)
            result += "\n"
        return result

    @staticmethod
    def init_matrix(data: list[list[Any]],
                    func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Matrix:
        matrix = Matrix(height=len(data), width=len(data[0]))
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                matrix.set_cell(x, y, cell=func(x, y, value, matrix))

        return matrix
