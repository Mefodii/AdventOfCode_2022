def is_unique(marker):
    return len(marker) == len(set(marker))


def find_non_repeating(line, step):
    for i in range(len(line)-step):
        marker = line[i:i+step]
        if is_unique(marker):
            return i + step

    return -1


###############################################################################
def run_a(input_data):
    result = find_non_repeating(input_data[0], 4)
    return result


def run_b(input_data):
    result = find_non_repeating(input_data[0], 14)
    return result
