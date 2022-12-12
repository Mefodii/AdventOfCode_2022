import math
from collections import Counter
from typing import Any


def list_to_int(data):
    return list(map(int, data))


def subtract_string_list(list1, list2):
    return list((Counter(list1) - Counter(list2)).elements())


def print_list(value):
    print(*value, sep="\n")
