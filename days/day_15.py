from __future__ import annotations

from typing import Tuple

from utils.Regex import findall_numbers
from utils.classes.Matrix import Cell, MatrixType, Matrix


class Sensor(Cell):
    def __init__(self, x: int, y: int, beacon: Beacon, matrix: MatrixType):
        super().__init__(x, y, "S", matrix)
        self.beacon = beacon
        self.distance = self.get_distance(beacon)

    def mark_row(self, y: int) -> None:
        def mark_direction(start_x: int, start_dist: int, mod: int):
            distance = start_dist
            x = start_x
            while distance <= self.distance and self.matrix.max_x >= x >= self.matrix.min_x:
                self.mark_cell(x, y)
                x += mod
                distance += 1

        y_dist = abs(y - self.y)
        mark_direction(self.x, y_dist, 1)
        mark_direction(self.x, y_dist, -1)

    def mark_cell(self, x: int, y: int) -> None:
        cell = self.matrix.get_cell_or_none(x, y)
        if cell is None:
            cell = Cell(x, y, "#", self.matrix)
            self.matrix.set_cell(x, y, cell)
            self.matrix.coverage += 1
        elif type(cell) is Cell and cell.value != "#":
            cell.value = "#"
            self.matrix.coverage += 1

    def __repr__(self):
        return f"{super().__repr__()} | beacon: {repr(self.beacon)} | Dist: {self.distance}"


class Beacon(Cell):
    def __init__(self, x: int, y: int, matrix: MatrixType):
        super().__init__(x, y, "B", matrix)


class Cave(Matrix):
    def __init__(self, min_x: int, min_y: int, max_x: int, max_y: int):
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        super().__init__(height, width, " ", min_x, min_y, lazy=True)
        self.sensors = []
        self.beacons = []
        self.coverage = 0

    def check_row(self, y: int):
        for sensor in self.sensors:
            sensor.mark_row(y)

    def check(self):
        for y in self.get_column_range():
            print(y)
            self.check_row(y)

    def get_first_free(self) -> Tuple[int, int] | None:
        for y in self.get_column_range():
            for x in self.get_row_range():
                if self.get_cell_or_none(x, y) is None:
                    return x, y

        return -1, -1

    def add_sensor(self, sensor: Sensor) -> None:
        self.sensors.append(sensor)
        self.set_cell(sensor.x, sensor.y, sensor)

    def add_beacon(self, beacon: Beacon) -> None:
        self.beacons.append(beacon)
        self.set_cell(beacon.x, beacon.y, beacon)


def init_cave(data) -> Cave:
    parsed_data = []
    x_list = []
    y_list = []
    for line in data:
        coords = findall_numbers(line)
        parsed_data.append(coords)
        x_list.append(coords[0])
        x_list.append(coords[2])
        y_list.append(coords[1])
        y_list.append(coords[3])

    min_x = min(x_list) - 1000000
    min_y = min(y_list) - 1000000
    max_x = max(x_list) + 1000000
    max_y = max(y_list) + 1000000

    cave = Cave(min_x, min_y, max_x, max_y)
    for coords in parsed_data:
        sx, sy, bx, by = coords

        cell = cave.get_cell_or_none(bx, by)
        if type(cell) is Beacon:
            beacon = cell
        else:
            beacon = Beacon(bx, by, cave)
            cave.add_beacon(beacon)

        cave.add_sensor(Sensor(sx, sy, beacon, cave))

    return cave


###############################################################################
def run_a(input_data, sample=False):
    cave = init_cave(input_data)

    y = 10 if sample else 2000000
    cave.check_row(y)
    return cave.coverage


def run_b(input_data, sample=False):
    cave = init_cave(input_data)

    cave.min_x = 0
    cave.min_y = 0
    if sample:
        cave.max_x = 20
        cave.max_y = 20
    else:
        cave.max_x = 4000000
        cave.max_y = 4000000

    cave.check()
    x, y = cave.get_first_free()
    result = 4000000 * x + y

    return result
