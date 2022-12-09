from __future__ import annotations
from utils.classes.Graph import Node


class File(Node):
    def __init__(self, value: str, size: int, parent: Dir):
        super().__init__(value)
        self.size = size
        super().add_parent(parent)


class Dir(Node):
    def __init__(self, value):
        super().__init__(value)
        self.size = 0
        self.dirs = []
        self.files = []

    def calculate_size(self) -> int:
        self.size = sum(d.calculate_size() for d in self.dirs) + sum(f.size for f in self.files)
        return self.size

    def add_dir(self, directory: Dir):
        self.dirs.append(directory)
        super().add_child(directory)

    def get_dir(self, value: str) -> Dir | None:
        for directory in self.dirs:
            if directory.value == value:
                return directory
        return None

    def add_file(self, file: File):
        self.files.append(file)
        super().add_child(file)

    def get_all_dirs(self, include_self=True):
        result = []
        if include_self:
            result.append(self)

        for directory in self.dirs:
            result.append(directory)
            result += directory.get_all_dirs(include_self=False)

        return result

    def __repr__(self):
        return f"{self.value} - {self.size}"


class Shell:
    CMD_LINE_FLAG = "$"
    CD = "cd"
    LS = "ls"

    CD_ROOT = "/"
    CD_BACK = ".."
    DIR = "dir"

    def __init__(self):
        self.root = Dir("/")
        self.cwd = self.root

    def interpret_output(self, output):
        buffer = []
        command = output[0]
        for line in output[1:]:
            if Shell.is_cmd_line(line):
                self.interpret_command(command, buffer)
                command = line
                buffer = []
            else:
                buffer.append(line)

        self.interpret_command(command, buffer)
        self.root.calculate_size()

    def interpret_command(self, command, buffer: list):
        args = command.split(" ")
        cmd = args[1]
        if cmd == Shell.CD:
            self.cd(args[2])
        if cmd == Shell.LS:
            self.ls(buffer)

    def cd(self, path: str):
        if path == Shell.CD_ROOT:
            self.cwd = self.root
        elif path == Shell.CD_BACK:
            self.cwd = self.cwd.parents[0]
        else:
            self.cwd = self.cwd.get_dir(path)

    def ls(self, buffer):
        for line in buffer:
            info, name = line.split(" ")
            if info == Shell.DIR:
                new_dir = Dir(name)
                new_dir.add_parent(self.cwd)
                self.cwd.add_dir(new_dir)
            else:
                self.cwd.add_file(File(name, int(info), self.cwd))

    @staticmethod
    def is_cmd_line(line):
        return line[0] == Shell.CMD_LINE_FLAG


def find_small_dirs(root: Dir, threshold):
    result = []
    dirs = root.get_all_dirs(include_self=True)
    for directory in dirs:
        if directory.size <= threshold:
            result.append(directory)
    return result


def find_dir_to_delete(root):
    total_space = 70000000
    required_space = 30000000

    min_required = required_space - (total_space - root.size)
    closest = total_space
    dirs = root.get_all_dirs(include_self=True)
    for directory in dirs:
        if min_required <= directory.size < closest:
            closest = directory.size
    return closest


###############################################################################
def run_a(input_data):
    shell = Shell()
    shell.interpret_output(input_data)
    small_dirs = find_small_dirs(shell.root, threshold=100000)
    result = sum(directory.size for directory in small_dirs)
    return result


def run_b(input_data):
    shell = Shell()
    shell.interpret_output(input_data)
    result = find_dir_to_delete(shell.root)
    return result
