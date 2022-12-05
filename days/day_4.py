class Assignment:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def contains(self, assignment):
        return self.start <= assignment.start and self.end >= assignment.end

    def overlap(self, assignment):
        return self.start <= assignment.start <= self.end or self.start <= assignment.end <= self.end

    def __repr__(self):
        return f'{self.start}-{self.end}'


def parse_assignments(data):
    assignments_groups = []
    for line in data:
        assignments = []
        args = line.split(",")
        for arg in args:
            start, end = arg.split("-")
            assignments.append(Assignment(int(start), int(end)))

        assignments_groups.append(assignments)

    return assignments_groups


def find_overlaps(assignments_groups):
    return list(filter(lambda group: group[0].overlap(group[1]) or group[1].overlap(group[0]), assignments_groups))


def find_fully_contained(assignments_groups):
    return list(filter(lambda group: group[0].contains(group[1]) or group[1].contains(group[0]), assignments_groups))


###############################################################################
def run_a(input_data):
    assignments_groups = parse_assignments(input_data)
    fully_contains = find_fully_contained(assignments_groups)
    result = len(fully_contains)
    return result


def run_b(input_data):
    assignments_groups = parse_assignments(input_data)
    overlaps = find_overlaps(assignments_groups)
    result = len(overlaps)
    return result
