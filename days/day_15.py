from __future__ import annotations

from utils.Regex import findall_numbers
from utils.classes.Matrix import Cell, MatrixType, Matrix, CellType


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

    def add_sensor(self, sensor: Sensor) -> None:
        self.sensors.append(sensor)
        self.set_cell(sensor.x, sensor.y, sensor)

    def add_beacon(self, beacon: Beacon) -> None:
        self.beacons.append(beacon)
        self.set_cell(beacon.x, beacon.y, beacon)

    def is_covered(self, x, y) -> bool:
        for sensor in self.sensors:
            distance = self.get_distance(sensor.x, sensor.y, x, y)
            if distance <= sensor.distance:
                return True

        return False


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

    min_x = min(x_list)
    min_y = min(y_list)
    max_x = max(x_list)
    max_y = max(y_list)

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
    # print(cave)

    covers = 0
    y = 10 if sample else 2000000
    cave.check_row(y)
    print(cave.coverage)
    # for x in cave.get_row_range():
    #     print(f"{x} / {cave.max_x}")
    #     covered = cave.is_covered(x, y)
    #     if covered:
    #         covers += 1
    # print(covers)
    return ""


def run_b(input_data, sample=False):
    return ""
