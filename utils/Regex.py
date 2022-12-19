import re

from utils.manipulators import list_to_int


def findall_numbers(line: str):
    return list_to_int(re.findall('-?[0-9]+', line))
