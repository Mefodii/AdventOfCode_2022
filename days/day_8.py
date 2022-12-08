from __future__ import annotations
import math

from utils.classes.Matrix import Matrix, Cell


class Tree(Cell):
    def __init__(self, x, y, value, matrix: Matrix):
        super().__init__(x, y, value, matrix)
        self.is_visible = False
        self.distances = []
        self.score = 0

    def calculate_visibility(self) -> bool:
        x = self.x
        y = self.y
        conditions = [self.matrix.is_edge(x, y)] + [self.is_side_visible(side) for side in self.matrix.get_sides(x, y)]
        self.is_visible = any(conditions)

        return self.is_visible

    def is_side_visible(self, side: list[Tree]) -> bool:
        return all(tree < self for tree in side)

    def calculate_distance(self):
        sides = self.matrix.get_sides(self.x, self.y)
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


###############################################################################
def run_a(input_data):
    trees = Matrix.init_matrix(input_data, func=lambda x, y, cell, matrix: Tree(x, y, int(cell), matrix))
    [item["cell"].calculate_visibility() for item in trees]
    result = len(list(filter(lambda t: t["cell"].is_visible, trees)))

    return result


def run_b(input_data):
    trees = Matrix.init_matrix(input_data, func=lambda x, y, cell, matrix: Tree(x, y, int(cell), matrix))
    [item["cell"].calculate_distance() for item in trees]
    result = max([item["cell"].score for item in trees])

    return result
