from __future__ import annotations
import math

from utils.classes.Matrix import Matrix, Cell


class Tree(Cell):
    def __init__(self, x, y, value):
        super().__init__(x, y, value)
        self.is_visible = False
        self.distances = []
        self.score = 0

    def calculate_visibility(self, trees: Matrix) -> bool:
        x = self.x
        y = self.y
        conditions = [trees.is_edge(x, y)] + [self.is_side_visible(side) for side in trees.get_sides(x, y)]
        self.is_visible = any(conditions)

        return self.is_visible

    def is_side_visible(self, side: list[Tree]) -> bool:
        return all(tree < self for tree in side)

    def calculate_distance(self, trees: Matrix):
        sides = trees.get_sides(self.x, self.y)
        sides[2] = sides[2][::-1]
        sides[3] = sides[3][::-1]

        self.distances = [self.calculate_side_distance(side) for side in sides]
        self.calculate_score()

    def calculate_side_distance(self, side: list[Tree]) -> int:
        return next((i + 1 for i in range(len(side)) if self.value <= side[i].value), len(side))

    def calculate_score(self) -> int:
        self.score = math.prod(self.distances)
        return self.score

    def __repr__(self):
        return f"{super().__repr__()}, score: {self.score}, dists:{self.distances}"


def calculate_visible(trees):
    [item["cell"].calculate_visibility(trees) for item in trees]


def calculate_distance(trees):
    [item["cell"].calculate_distance(trees) for item in trees]


###############################################################################
def run_a(input_data):
    trees = Matrix.init_matrix(input_data, func=lambda x, y, cell: Tree(x, y, int(cell)))
    calculate_visible(trees)
    result = len(list(filter(lambda t: t["cell"].is_visible, trees)))

    return result


def run_b(input_data):
    trees = Matrix.init_matrix(input_data, func=lambda x, y, cell: Tree(x, y, int(cell)))
    calculate_distance(trees)
    result = max([item["cell"].score for item in trees])

    return result
