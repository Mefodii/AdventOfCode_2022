def get_priority(item):
    base = ord("a") - 1
    if item.isupper():
        base = ord("A") - 27
    return ord(item) - base


def find_common_item(data):
    # print(data)
    res = set(data[0])

    for temp in data[1:]:
        res = res.intersection(temp)
        # print(res)

    return res.pop()


def parse_rucksacks(data):
    total_priority = 0
    for rucksack in data:
        size = len(rucksack)
        comp1 = rucksack[0:size//2]
        comp2 = rucksack[size//2:]

        common_item = find_common_item([comp1, comp2])
        total_priority += get_priority(common_item)

    return total_priority


def parse_groups(data):
    total_priority = 0
    for i in range(0, len(data), 3):
        group = data[i:i+3]

        common_item = find_common_item(group)
        total_priority += get_priority(common_item)

    return total_priority


###############################################################################
def run_a(input_data):
    result = parse_rucksacks(input_data)
    return result


def run_b(input_data):
    result = parse_groups(input_data)
    return result
