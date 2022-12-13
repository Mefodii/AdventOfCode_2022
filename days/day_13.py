from __future__ import annotations

import ast

from utils.Validation import is_int

RIGHT_ORDER = -1
WRONG_ORDER = 1
CONTINUE = 0


class Signal:
    def __init__(self, stm: str):
        self.stm = stm
        self.data = ast.literal_eval(stm)

    def __repr__(self):
        return self.stm

    @staticmethod
    def check_pair(left, right) -> int:
        for i in range(min(len(left), len(right))):
            left_element = left[i]
            right_element = right[i]

            left_int = is_int(left_element)
            right_int = is_int(right_element)

            if left_int and right_int:
                if left_element < right_element:
                    return RIGHT_ORDER
                elif left_element > right_element:
                    return WRONG_ORDER
            elif (not left_int and right_int) or (left_int and not right_int):
                if right_int:
                    right_list = [right_element]
                    left_list = left_element
                else:
                    right_list = right_element
                    left_list = [left_element]

                result = Signal.check_pair(left_list, right_list)
                if result != CONTINUE:
                    return result
            else:
                result = Signal.check_pair(left_element, right_element)
                if result != CONTINUE:
                    return result

        if len(left) < len(right):
            return RIGHT_ORDER
        if len(left) > len(right):
            return WRONG_ORDER

        return CONTINUE

    def compare(self, other: Signal) -> int:
        return Signal.check_pair(self, other)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __lt__(self, other):
        return self.compare(other) == -1

    def __eq__(self, other):
        return self.compare(other) == 0


def build_pairs(data: list[str]) -> list[list[Signal, Signal]]:
    pairs = []
    for i in range(0, len(data), 3):
        left = Signal(data[i])
        right = Signal(data[i + 1])
        pairs.append([left, right])
    return pairs


def parse_pairs(pairs: list[list[Signal, Signal]]) -> list[int]:
    indexes = []
    for i, pair in enumerate(pairs):
        if pair[0] < pair[1]:
            indexes.append(i + 1)

    return indexes


###############################################################################
def run_a(input_data):
    pairs = build_pairs(input_data)
    indexes = parse_pairs(pairs)
    return sum(indexes)


def run_b(input_data):
    pairs = build_pairs(input_data)
    two = Signal("[[2]]")
    six = Signal("[[6]]")
    signals = [two, six]
    for pair in pairs:
        signals.append(pair[0])
        signals.append(pair[1])

    signals.sort()
    result = (signals.index(two) + 1) * (signals.index(six) + 1)
    return result
