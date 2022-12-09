from __future__ import annotations
from utils.classes.Matrix import Direction, UP, DOWN, LEFT, RIGHT, MOVE


class Knot:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visits = {str(x) + " " + str(y): True}
        self.child = None

    def move(self, direction: Direction, distance: int):
        for _ in range(distance):
            self.x, self.y = MOVE[direction](self.x, self.y, 1)
            self.visits[str(self.x) + " " + str(self.y)] = True
            if self.child:
                self.child.follow(self.x, self.y)

    def follow(self, x: int, y: int):
        x_dist = x - self.x
        y_dist = y - self.y

        move_direction = ""

        move_direction += UP if y_dist < -1 or (y_dist < 0 and abs(x_dist) > 1) else ""
        move_direction += DOWN if y_dist > 1 or (y_dist > 0 and abs(x_dist) > 1) else ""
        move_direction += RIGHT if x_dist > 1 or (x_dist > 0 and abs(y_dist) > 1) else ""
        move_direction += LEFT if x_dist < -1 or (x_dist < 0 and abs(y_dist) > 1) else ""

        if len(move_direction) != 0:
            self.move(Direction(move_direction), 1)

    def __repr__(self):
        return f"{self.x} {self.y}"


def init_rope(len_knots: int):
    rope = [Knot(0, 0) for _ in range(len_knots + 1)]

    for i in range(len(rope) - 1):
        rope[i].child = rope[i + 1]

    return rope


def simulate(data: list[str], len_knots: int) -> int:
    rope = init_rope(len_knots)
    head = rope[0]
    for move in data:
        direction, distance = move.split(" ")
        head.move(Direction(direction), int(distance))

    tail = rope[-1]
    visits = len(tail.visits.values())
    return visits


###############################################################################
def run_a(input_data):
    return simulate(input_data, 1)


def run_b(input_data):
    return simulate(input_data, 9)
