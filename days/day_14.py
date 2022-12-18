from __future__ import annotations
from typing import Tuple

from utils.classes.Matrix import Cell, Matrix, Direction, CellType


class Sand(Cell):
    def __init__(self, x: int, y: int, matrix: Cave):
        super().__init__(x, y, "o", matrix)

    def fall(self) -> Tuple[int | None, int | None]:
        while True:
            self.drop()
            if self.y is None:
                break

            down_left, down_right = self.get_down_corners()
            if down_left is not None and type(down_left) is Cell:
                self.x, self.y = down_left.get_coords()
            elif down_right is not None and type(down_right) is Cell:
                self.x, self.y = down_right.get_coords()
            elif down_right is None or down_left is None:
                self.x = None
                break
            else:
                break

        return self.x, self.y

    def drop(self) -> int | None:
        column = self.matrix.get_column(self.x)
        for cell in column[self.y:]:
            if isinstance(cell, (Sand, Rock)):
                self.y = cell.y - 1
                return self.y

        self.y = None
        return self.y

    def get_down_corners(self) -> Tuple[CellType | None, CellType | None]:
        return self.get_neighbour(Direction.DOWN_LEFT), self.get_neighbour(Direction.DOWN_RIGHT)


class Rock(Cell):
    pass


class Cave(Matrix):
    SAND_ORIGIN_X = 500
    SAND_ORIGIN_Y = 0

    def __init__(self, height: int, width: int):
        super().__init__(height, width, init_value=" ")
        self.sands = 0
        self.balanced = False

    def produce_sand(self) -> None:
        sand = Sand(self.SAND_ORIGIN_X, self.SAND_ORIGIN_Y, self)
        x, y = sand.fall()
        if None in (x, y):
            self.balanced = True
            return

        if x == self.SAND_ORIGIN_X and y == self.SAND_ORIGIN_Y:
            self.sands += 1
            self.balanced = True
            return

        self.sands += 1
        self.set_cell(x, y, sand)

    def add_rocks(self, coords):
        for i in range(len(coords) - 1):
            start = coords[i]
            end = coords[i + 1]
            self.add_rock_line(start[0], start[1], end[0], end[1])

    def add_rock_line(self, x1, y1, x2, y2):
        x_mod = 0 if x1 == x2 else 1 if x1 < x2 else -1
        y_mod = 0 if y1 == y2 else 1 if y1 < y2 else -1

        x = x1
        y = y1
        while True:
            rock = Rock(x, y, "#", self)
            self.set_cell(x, y, rock)

            if x2 == x and y2 == y:  # We need to add rock on last x, y as well
                break

            x += x_mod
            y += y_mod


def init_cave(data):
    rocks = []
    for line in data:
        rocks.append([list(map(lambda n: int(n), p.split(","))) for p in line.split(" -> ")])

    x_list = []
    y_list = []
    for coords in rocks:
        for point in coords:
            x_list.append(point[0])
            y_list.append(point[1])

    height = max(y_list) + 3
    width = Cave.SAND_ORIGIN_X + height
    cave = Cave(height, width)
    for coords in rocks:
        cave.add_rocks(coords)
    return cave


###############################################################################
def run_a(input_data):
    cave = init_cave(input_data)
    while not cave.balanced:
        cave.produce_sand()
    return cave.sands


def run_b(input_data):
    cave = init_cave(input_data)
    cave.add_rock_line(0, cave.height - 1, cave.width - 1, cave.height - 1)
    while not cave.balanced:
        cave.produce_sand()
    return cave.sands
