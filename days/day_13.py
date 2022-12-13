from __future__ import annotations
import ast


def build_pairs(data):
    pairs = []
    for i in range(0, len(data), 3):
        left = ast.literal_eval(data[i])
        right = ast.literal_eval(data[i + 1])
        pairs.append([left, right])
    return pairs


###############################################################################
def run_a(input_data):
    pairs = build_pairs(input_data)
    print(pairs)
    return ""


def run_b(input_data):
    return ""
