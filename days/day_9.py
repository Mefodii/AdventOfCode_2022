from __future__ import annotations
from utils.classes.Matrix import Direction, DIRECTIONS, UP, DOWN, LEFT, RIGHT

moves = {
    Direction.UP: lambda x, y, dist: [x, y - dist],
    Direction.DOWN: lambda x, y, dist: [x, y + dist],
    Direction.LEFT: lambda x, y, dist: [x - dist, y],
    Direction.RIGHT: lambda x, y, dist: [x + dist, y],
    Direction.UP_LEFT: lambda x, y, dist: [x - dist, y - dist],
    Direction.UP_RIGHT: lambda x, y, dist: [x + dist, y - dist],
    Direction.DOWN_LEFT: lambda x, y, dist: [x - dist, y + dist],
    Direction.DOWN_RIGHT: lambda x, y, dist: [x + dist, y + dist],
}


class Head:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.knot = None

    def move(self, direction: Direction, distance: int):
        for _ in range(distance):
            self.x, self.y = moves[direction](self.x, self.y, 1)
            self.knot.follow_parent()

    def __repr__(self):
        return f"{self.x} {self.y}"


class Knot:
    def __init__(self, x: int, y: int, parent: Head | Knot):
        self.x = x
        self.y = y
        self.visits = {str(x) + " " + str(y): True}
        self.parent = parent
        self.knot = None

    def move(self, direction: Direction, distance: int) -> [int, int]:
        self.x, self.y = moves[direction](self.x, self.y, distance)
        self.visits[str(self.x) + " " + str(self.y)] = True
        if self.knot:
            self.knot.follow_parent()

        return self.x, self.y

    def follow_parent(self):
        self.follow(self.parent.x, self.parent.y)

    def follow(self, x: int, y: int):
        x_dist = x - self.x
        y_dist = y - self.y
        while abs(x_dist) > 1 or abs(y_dist) > 1:
            move_direction = ""

            move_direction += UP if y_dist < -1 or y_dist < 0 and abs(x_dist) > 1 else ""
            move_direction += DOWN if y_dist > 1 or y_dist > 0 and abs(x_dist) > 1 else ""
            move_direction += RIGHT if x_dist > 1 or x_dist > 0 and abs(y_dist) > 1 else ""
            move_direction += LEFT if x_dist < -1 or x_dist < 0 and abs(y_dist) > 1 else ""

            self.move(DIRECTIONS[move_direction], 1)
            x_dist = x - self.x
            y_dist = y - self.y

    def __repr__(self):
        return f"{self.x} {self.y}"


def init_rope(len_knots: int):
    rope = [Head(0, 0)]
    for _ in range(len_knots):
        rope.append(Knot(0, 0, rope[-1]))

    for i in range(len(rope) - 1):
        rope[i].knot = rope[i + 1]

    head, knots = rope[0], rope[1:]
    return head, knots


def simulate(data: list[str], len_knots: int) -> int:
    head, knots = init_rope(len_knots)
    for move in data:
        args = move.split(" ")
        direction = DIRECTIONS[args[0]]
        distance = int(args[1])

        head.move(direction, int(distance))

    tail = knots[-1]
    visits = len(tail.visits.values())
    return visits


###############################################################################
def run_a(input_data):
    visits = simulate(input_data, 1)
    return visits


def run_b(input_data):
    visits = simulate(input_data, 9)
    return visits
