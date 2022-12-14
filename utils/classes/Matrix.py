from __future__ import annotations
from enum import Enum

from typing import Callable, Any, TypeVar, Self, Tuple

MatrixType = TypeVar('MatrixType', bound='Matrix')
CellType = TypeVar('CellType', bound='Cell')

UP = "U"
DOWN = "D"
LEFT = "L"
RIGHT = "R"
UP_RIGHT = "UR"
UP_LEFT = "UL"
DOWN_RIGHT = "DR"
DOWN_LEFT = "DL"


class Direction(Enum):
    UP = UP
    DOWN = DOWN
    LEFT = LEFT
    RIGHT = RIGHT
    UP_RIGHT = UP_RIGHT
    UP_LEFT = UP_LEFT
    DOWN_RIGHT = DOWN_RIGHT
    DOWN_LEFT = DOWN_LEFT


MOVE = {
    Direction.UP: lambda x, y, dist: [x, y - dist],
    Direction.DOWN: lambda x, y, dist: [x, y + dist],
    Direction.LEFT: lambda x, y, dist: [x - dist, y],
    Direction.RIGHT: lambda x, y, dist: [x + dist, y],
    Direction.UP_LEFT: lambda x, y, dist: [x - dist, y - dist],
    Direction.UP_RIGHT: lambda x, y, dist: [x + dist, y - dist],
    Direction.DOWN_LEFT: lambda x, y, dist: [x - dist, y + dist],
    Direction.DOWN_RIGHT: lambda x, y, dist: [x + dist, y + dist],
}


class Cell:
    def __init__(self, x: int, y: int, value: Any, matrix: MatrixType):
        self.x = x
        self.y = y
        self.value = value
        self.matrix = matrix

    def get_coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def get_neighbour(self, direction: Direction) -> CellType | None:
        return self.matrix.get_neighbour(self.x, self.y, direction)

    def is_edge(self) -> bool:
        return self.matrix.is_edge(self.x, self.y)

    def get_sides(self) -> list[list[Self]]:
        """Get in line all sides from current coordinates. Clockwise, starting from right side (R,B,L,T)"""
        return self.matrix.get_sides(self.x, self.y)

    def get_distance(self, cell: CellType):
        return Matrix.get_distance(self.x, self.y, cell.x, cell.y)

    def __repr__(self):
        return f'{self.x}, {self.y} value: {self.value}'

    def __lt__(self, other: Self):
        return self.value.__lt__(other.value)

    def __le__(self, other: Self):
        return self.value.__le__(other.value)

    def __gt__(self, other: Self):
        return self.value.__gt__(other.value)

    def __ge__(self, other: Self):
        return self.value.__ge__(other.value)

    def __eq__(self, other: Self):
        return self.value.__eq__(other.value)

    def __ne__(self, other: Self):
        return self.value.__ne__(other.value)


class Matrix:
    def __init__(self, height: int, width: int, init_value: Any = None, min_x: int = 0, min_y: int = 0,
                 lazy: bool = False):
        self.height = height
        self.width = width
        self.init_value = init_value

        self.min_x = min_x
        self.min_y = min_y
        self.max_x = width + min_x - 1
        self.max_y = height + min_y - 1

        self.matrix = {}

        self.lazy = lazy
        if lazy:
            return

        for y in self.get_column_range():
            row = {}
            for x in self.get_row_range():
                row[x] = Cell(x, y, init_value, self)
            self.matrix[y] = row

    def map_data(self, data: list[list[Any]],
                 func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        for y, row in enumerate(data):
            for x, value in enumerate(row):
                self.set_cell(x, y, cell=func(x, y, value, self))

        return self

    def get_data(self) -> list[list[Any]]:
        data = []
        for y in self.get_column_range():
            data.append([cell.value for cell in self.get_row(y)])

        return data

    def get_column_range(self) -> range:
        return range(self.min_y, self.max_y + 1)

    def get_row_range(self) -> range:
        return range(self.min_x, self.max_x + 1)

    def append_right(self, cell_func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        """Creates new column at the right"""
        self.width += 1
        self.max_x += 1
        x = self.max_x

        [self.set_cell(x, y, cell_func(x, y, self.init_value, self)) for y in self.get_column_range()]
        return self

    def append_left(self, cell_func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        """Creates new column at the left"""
        self.width += 1
        self.min_x -= 1
        x = self.min_x

        [self.set_cell(x, y, cell_func(x, y, self.init_value, self)) for y in self.get_column_range()]
        return self

    def append_bottom(self, cell_func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        """Creates new row at the bottom"""
        self.height += 1
        self.max_y += 1
        y = self.max_y
        self.matrix[y] = {}

        for x in self.get_row_range():
            self.set_cell(x, y, cell_func(x, y, self.init_value, self))
        return self

    def append_top(self, cell_func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        """Creates new row at the top"""
        self.height += 1
        self.min_y -= 1
        y = self.min_y
        self.matrix[y] = {}

        for x in self.get_row_range():
            self.set_cell(x, y, cell_func(x, y, self.init_value, self))
        return self

    @staticmethod
    def get_distance(x1: int, y1: int, x2: int, y2: int) -> int:
        x_dist = abs(x1 - x2)
        y_dist = abs(y1 - y2)
        return x_dist + y_dist

    def get_neighbour(self, x, y, direction: Direction) -> CellType | None:
        x1, y1 = MOVE[direction](x, y, 1)
        return self.get_cell_or_none(x1, y1)

    def get_adjacent(self, x: int, y: int, diagonal: bool = False) -> dict[Direction, CellType]:
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

    def get_row(self, y: int) -> list[CellType]:
        return [self.get_cell(x, y) for x in self.get_row_range()]

    def get_column(self, x: int) -> list[CellType]:
        return [self.get_cell(x, y) for y in self.get_column_range()]

    def get_left(self, x: int, y: int) -> list[CellType]:
        return self.get_row(y)[:x - self.min_x]

    def get_right(self, x: int, y: int) -> list[CellType]:
        return self.get_row(y)[x + 1 - self.min_x:]

    def get_top(self, x: int, y: int) -> list[CellType]:
        return self.get_column(x)[:y - self.min_y]

    def get_bottom(self, x: int, y: int) -> list[CellType]:
        return self.get_column(x)[y + 1 - self.min_y:]

    def get_sides(self, x: int, y: int) -> list[list[CellType]]:
        """Get in line all sides from current coordinates. Clockwise, starting from right side (R,B,L,T)"""
        return [
            self.get_right(x, y),
            self.get_bottom(x, y),
            self.get_left(x, y),
            self.get_top(x, y),
        ]

    def get_cell(self, x: int, y: int) -> CellType:
        return self.matrix[y][x]

    def set_cell(self, x: int, y: int, cell: CellType):
        if not self.min_x <= x <= self.max_x:
            raise Exception(f"x: {x} out of bounds")
        if not self.min_y <= y <= self.max_y:
            raise Exception(f"y: {y} out of bounds")

        row = self.matrix.get(y, None)
        if not row:
            row = {}
            self.matrix[y] = row
        row[x] = cell

    def get_value(self, x: int, y: int) -> Any:
        return self.get_cell(x, y).value

    def set_value(self, x: int, y: int, value: Any):
        self.get_cell(x, y).value = value

    def get_cell_or_none(self, x: int, y: int) -> CellType | None:
        return self.matrix.get(y, {}).get(x, None)

    def is_edge(self, x: int, y: int) -> bool:
        return x == self.min_x or x == self.max_x or y == self.min_y or y == self.max_y

    def __copy__(self) -> Self:
        obj = type(self)(self.height, self.width, self.init_value)
        obj.map_data(self.get_data())
        return obj

    def __iter__(self) -> Self:
        self.current_x = self.min_x
        self.current_y = self.min_y
        return self

    def __next__(self) -> CellType:
        if self.current_x >= self.width:
            self.current_x = self.min_x
            self.current_y += 1

        if self.current_y >= self.height:
            raise StopIteration

        cell = self.get_cell(self.current_x, self.current_y)
        self.current_x += 1

        return cell

    def __repr__(self) -> str:
        if self.lazy:
            return f"Matrix is in lazy mode, cannot print"

        result = ""
        for y in self.get_column_range():
            for x in self.get_row_range():
                result += str(self.get_cell(x, y).value)
            result += "\r\n"
        return result

    @classmethod
    def init_matrix(cls, data: list[list[Any]],
                    func: Callable = lambda x, y, value, matrix: Cell(x, y, value, matrix)) -> Self:
        matrix = cls(height=len(data), width=len(data[0]))
        matrix.map_data(data, func)
        return matrix
