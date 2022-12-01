def calculate_sorted_totals(elfs_inventory):
    totals = []
    for elf_inventory in elfs_inventory:
        total_calories = sum(elf_inventory)
        totals.append(total_calories)

    totals.sort(reverse=True)
    return totals


def find_most_calories_inventory(elfs_inventory):
    biggest = 0
    for elf_inventory in elfs_inventory:
        total_calories = sum(elf_inventory)
        biggest = max(total_calories, biggest)

    return biggest


def split_inventory(data):
    elfs_inventory = []
    buffer = []
    for item in data:
        if len(item) == 0:
            elfs_inventory.append(buffer)
            buffer = []
        else:
            buffer.append(int(item))

    elfs_inventory.append(buffer)
    return elfs_inventory


###############################################################################
def run_a(input_data):
    elfs_inventory = split_inventory(input_data)
    most_calories_inventory = find_most_calories_inventory(elfs_inventory)
    return most_calories_inventory


def run_b(input_data):
    elfs_inventory = split_inventory(input_data)
    totals = calculate_sorted_totals(elfs_inventory)
    result = sum(totals[:3])
    return result
