class Action:
    def __init__(self, count, stack_id_from, stack_id_to, reverse):
        self.count = count
        self.stack_id_from = stack_id_from
        self.stack_id_to = stack_id_to
        self.reverse = reverse

    @staticmethod
    def build_obj(raw_data, reverse):
        args = raw_data.split(" ")
        count = int(args[1])
        stack_id_from = int(args[3])
        stack_id_to = int(args[5])

        return Action(count, stack_id_from, stack_id_to, reverse)

    def __repr__(self):
        return f'Move {self.count} from {self.stack_id_from} to {self.stack_id_to}'


class Stack:
    def __init__(self, id, crates):
        self.id = id
        self.crates = crates

    def put(self, crates):
        self.crates += crates

    def peek(self):
        if len(self.crates) > 0:
            return self.crates[-1]
        return ""

    def take(self, count):
        end = len(self.crates) - count
        result = self.crates[end:]

        if end == 0:
            self.crates = ""
        else:
            self.crates = self.crates[0:end]

        return result

    def __repr__(self):
        return f'Stack {self.id} with {self.crates}'


def init_stacks(data):
    total_stacks = len(data[-1].replace(" ", ""))
    stacks = [Stack(i + 1, "") for i in range(total_stacks)]

    for line in data[0:-1][::-1]:
        for i in range(total_stacks):
            crate_pos = 4 * i + 1
            if crate_pos <= len(line):
                crate = line[crate_pos]
                if crate != " ":
                    stacks[i].put(crate)

    return stacks


def init_actions(data, reverse):
    actions = [Action.build_obj(line, reverse) for line in data]
    return actions


def parse_input(data, reverse):
    sep_pos = 0
    for i in range(len(data)):
        if len(data[i]) == 0:
            sep_pos = i
            break

    stacks = init_stacks(data[0:sep_pos])
    actions = init_actions(data[sep_pos+1:], reverse)
    return [stacks, actions]


def execute_actions(stacks, actions):
    for action in actions:
        stack_from = stacks[action.stack_id_from - 1]
        stack_to = stacks[action.stack_id_to - 1]
        crates = stack_from.take(action.count)
        if action.reverse:
            crates = crates[::-1]
        stack_to.put(crates)


###############################################################################
def run_a(input_data):
    stacks, actions = parse_input(input_data, reverse=True)
    execute_actions(stacks, actions)
    result = "".join([stack.peek() for stack in stacks])
    return result


def run_b(input_data):
    stacks, actions = parse_input(input_data, reverse=False)
    execute_actions(stacks, actions)
    result = "".join([stack.peek() for stack in stacks])
    return result
