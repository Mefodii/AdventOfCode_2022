from __future__ import annotations

from math import lcm
from typing import Callable

from utils.Regex import findall_numbers

OPERATION = "  Operation: new = "


class Item:
    def __init__(self, worry: int):
        self.worry = worry

    def __repr__(self):
        return f"{self.worry}"


class Monkey:
    def __init__(self, name: int, worry_reduction: int = 3):
        self.name = name
        self.operation: Callable = lambda worry: worry
        self.items: list[Item] = []
        self.divisible_test: int = 0
        self.test_true_monkey: Monkey | None = None
        self.test_false_monkey: Monkey | None = None
        self.total_inspects: int = 0
        self.worry_reduction = worry_reduction
        self.lcm = 1

    def round(self):
        for item in self.items:
            item.worry = (self.operation(item.worry) // self.worry_reduction) % self.lcm
            monkey = self.test_true_monkey if item.worry % self.divisible_test == 0 else self.test_false_monkey
            monkey.catch(item)

        self.total_inspects += len(self.items)
        self.items = []

    def catch(self, item):
        self.items.append(item)

    def __repr__(self):
        return f"Monkey: {self.name}, Items: {self.items}, Test: {self.divisible_test}, " \
               f"True: {self.test_true_monkey.name}, False: {self.test_false_monkey.name}"


def run_round(monkeys):
    [monkey.round() for monkey in monkeys]


def init_monkeys(raw_monkeys: list[list[str]]):
    monkeys = [Monkey(i) for i in range(len(raw_monkeys))]
    total_lcm = 1
    for i, raw_monkey in enumerate(raw_monkeys):
        monkey = monkeys[i]
        monkey.items = [Item(worry) for worry in findall_numbers(raw_monkey[1])]
        monkey.divisible_test = findall_numbers(raw_monkey[3])[0]
        total_lcm = lcm(total_lcm, monkey.divisible_test)
        monkey.test_true_monkey = monkeys[findall_numbers(raw_monkey[4])[0]]
        monkey.test_false_monkey = monkeys[findall_numbers(raw_monkey[5])[0]]

        def new_op(o):
            return lambda old: eval(o)

        operation = raw_monkey[2].replace(OPERATION, "")
        monkey.operation = new_op(operation)

    for monkey in monkeys:
        monkey.lcm = total_lcm

    return monkeys


def split_input(data):
    raw_monkeys = []
    raw_monkey = []
    for line in data:
        if not line:
            raw_monkeys.append(raw_monkey)
            raw_monkey = []
            continue

        raw_monkey.append(line)

    raw_monkeys.append(raw_monkey)
    return raw_monkeys


###############################################################################
def run_a(input_data):
    monkeys = init_monkeys(split_input(input_data))
    [run_round(monkeys) for i in range(20)]
    inspects = [m.total_inspects for m in monkeys]
    inspects.sort()
    return inspects[-1] * inspects[-2]


def run_b(input_data):
    monkeys = init_monkeys(split_input(input_data))
    for m in monkeys:
        m.worry_reduction = 1

    [run_round(monkeys) for i in range(10000)]
    inspects = [m.total_inspects for m in monkeys]
    inspects.sort()
    return inspects[-1] * inspects[-2]
