from __future__ import annotations

import sys
from typing import Any, Callable, Type, Self

from utils.classes.Matrix import Matrix, Cell, Direction

START = ord("a")
END = ord("z")


class Elevation(Cell):

    def __init__(self, x, y, value, matrix: Maze):
        super().__init__(x, y, value, matrix)
        self.is_start = False
        self.is_end = False
        self.dist = -1

    def __repr__(self):
        return super().__repr__() + f", Dist: {self.dist}"

    def __hash__(self):
        return hash(repr(self))

    def get_adjacent(self) -> dict[Direction, Self]:
        return self.matrix.get_adjacent(self.x, self.y)

    def is_visited(self) -> bool:
        return self.dist >= 0

    def get_elevation(self) -> int:
        if self.is_start:
            return START
        if self.is_end:
            return END

        return ord(self.value)

    def can_move(self, c: Self) -> bool:
        v1 = self.get_elevation()
        v2 = c.get_elevation()
        return v2 - v1 <= 1

    def is_accessible(self, dist) -> bool:
        for adjacent in self.get_adjacent().values():
            if adjacent and adjacent.is_visited() and adjacent.can_move(self) and dist != adjacent.dist:
                return True

        return False

    def get_non_visited_adjacent(self) -> list[Self]:
        result = []
        for adjacent in self.get_adjacent().values():
            if adjacent and not adjacent.is_visited():
                result.append(adjacent)

        return result


class Maze(Matrix):

    def __init__(self, height: int, width: int, init_value: Any = None):
        super().__init__(height, width, init_value)
        self.start = None
        self.end = None
        self.dist = sys.maxsize

    def get_a_cells(self) -> list[Elevation]:
        result = []
        for y in self.get_column_range():
            for x in self.get_row_range():
                if self.get_value(x, y) == "a":
                    result.append(self.get_cell(x, y))
        return result

    def reset(self):
        for y in self.get_column_range():
            for x in self.get_row_range():
                self.get_cell(x, y).dist = -1

    def switch_start(self, cell):
        self.start.is_start = False
        self.start.dist = -1

        self.start = cell
        self.start.is_start = True
        self.start.dist = 0

    def map_data(self, data: list[list[Any]],
                 func: Callable = lambda x, y, value, matrix: Elevation(x, y, value, matrix)):
        super().map_data(data, func)
        for y, line in enumerate(data):
            if "S" in line:
                x = line.index("S")
                self.start = self.get_cell(x, y)
                self.start.is_start = True
                self.start.dist = 0

            if "E" in line:
                x = line.index("E")
                self.end = self.get_cell(x, y)
                self.end.is_end = True

    def find_shortest_path(self):
        buffer = set()
        buffer.update(self.start.get_non_visited_adjacent())
        dist = 1
        stuck = False

        while not self.end.is_visited() and not stuck and dist < self.dist:
            stuck = True
            new_buffer = set()
            for elevation in buffer:
                if elevation.is_accessible(dist):
                    stuck = False
                    elevation.dist = dist
                    new_buffer.update(elevation.get_non_visited_adjacent())
                else:
                    new_buffer.add(elevation)

            dist += 1
            buffer = new_buffer

        if self.end.is_visited():
            self.dist = self.end.dist

    @classmethod
    def init_matrix(cls: Maze, data: list[list[Any]],
                    func: Callable = lambda x, y, value, matrix: Elevation(x, y, value, matrix)) -> Maze:
        matrix = Maze(height=len(data), width=len(data[0]))
        matrix.map_data(data, func)
        return matrix


###############################################################################
def run_a(input_data):
    maze = Maze.init_matrix(input_data)
    maze.find_shortest_path()
    return maze.end.dist


def run_b(input_data):
    maze = Maze.init_matrix(input_data)
    for cell in maze.get_a_cells():
        maze.reset()
        maze.switch_start(cell)
        maze.find_shortest_path()

    return maze.dist
