from __future__ import annotations

from utils.classes.Matrix import Matrix

NOOP = "noop"
ADDX = "addx"


class CPU:
    PRINTABLE_CYCLES = [20, 60, 100, 140, 180, 220, 260]

    def __init__(self):
        self.cycle = 1
        self.value = 1
        self.instructions = []
        self.signal_strength = 0

        self.width = 40
        self.height = 6
        self.crt = Matrix(self.height, self.width, " ")

    def run_instructions_a(self):
        crt_line = 0
        for instruction in self.instructions:
            next_cycle = self.cycle + instruction.duration

            if self.PRINTABLE_CYCLES[crt_line] < next_cycle:
                self.signal_strength += self.PRINTABLE_CYCLES[crt_line] * self.value
                crt_line += 1

            instruction.execute(self)

            if self.cycle in self.PRINTABLE_CYCLES:
                self.signal_strength += self.PRINTABLE_CYCLES[crt_line] * self.value
                crt_line += 1

    def run_instructions_b(self):
        crt_line = 0
        crt_pos = 0
        for instruction in self.instructions:
            for i in range(instruction.duration):
                value = "#" if self.value - 1 <= crt_pos <= self.value + 1 else " "
                self.crt.set_value(crt_pos, crt_line, value)
                crt_pos = (crt_pos + 1) % self.width

                if crt_pos == 0:
                    crt_line += 1

            instruction.execute(self)

    def __repr__(self):
        return f"cycle: {self.cycle}, value: {self.value}"


class Instruction:
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration

    def execute(self, cpu: CPU):
        cpu.cycle += self.duration

    def __repr__(self):
        return f"{self.name}"


class InstructionNoop(Instruction):
    def __init__(self):
        super().__init__(NOOP, 1)


class InstructionAddx(Instruction):
    def __init__(self, value: int):
        super().__init__(ADDX, 2)
        self.value = value

    def execute(self, cpu: CPU):
        super().execute(cpu)
        cpu.value += self.value

    def __repr__(self):
        return super().__repr__() + f" {self.value}"


def create_instruction(raw_instruction):
    args = raw_instruction.split(" ")
    name = args[0]
    if name == NOOP:
        return InstructionNoop()

    if name == ADDX:
        return InstructionAddx(int(args[1]))


###############################################################################
def run_a(input_data):
    cpu = CPU()
    cpu.instructions = [create_instruction(line) for line in input_data]
    cpu.run_instructions_a()
    return cpu.signal_strength


def run_b(input_data):
    cpu = CPU()
    cpu.instructions = [create_instruction(line) for line in input_data]
    cpu.run_instructions_b()
    return cpu.crt
