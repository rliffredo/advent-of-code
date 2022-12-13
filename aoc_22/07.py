import itertools
from dataclasses import dataclass, field
from typing import List, Optional, Dict

from common import read_data


@dataclass
class Directory:
    name: str
    size: int = 0
    parent: Optional['Directory'] = None
    directories: Dict[str, 'Directory'] = field(default_factory=dict)

    @property
    def subs(self):
        return self.directories.values()

    @property
    def total_size(self):
        return sum(d.total_size for d in self.subs) + self.size

    @property
    def is_dir(self):
        return self.size == 0

    @staticmethod
    def parse_terminal_output(lines: List[str]) -> 'Directory':
        root = Directory(name='/')
        current_dir = None
        for line in lines:
            match line.split():
                case ['$', 'cd', '/']:
                    current_dir = root
                case ['$', 'cd', '..']:
                    current_dir = current_dir.parent
                case ['$', 'cd', name]:
                    current_dir = current_dir.directories[name]
                case ['$', 'ls']:
                    pass
                case ['dir', name]:
                    current_dir.directories[name] = Directory(name=name, parent=current_dir)
                case [size, name]:
                    current_dir.directories[name] = Directory(name=name, size=int(size))
        return root


def get_sizes(tree, predicate):
    sizes = [tree.total_size] if tree.is_dir and predicate(tree) else []
    sizes.extend(itertools.chain.from_iterable(get_sizes(d, predicate) for d in tree.subs))
    return sizes


def part_1() -> int:
    lines = read_data('07', True)
    tree = Directory.parse_terminal_output(lines)

    return sum(get_sizes(tree, lambda d: d.total_size < 100000))


def part_2() -> int:
    lines = read_data('07', True)
    tree = Directory.parse_terminal_output(lines)

    free_space = 70000000 - tree.total_size
    needed_space = 30000000 - free_space

    return sorted(get_sizes(tree, lambda d: d.total_size >= needed_space))[0]


SOLUTION_1 = 1086293
SOLUTION_2 = 366028

if __name__ == '__main__':
    print(part_1())
    print(part_2())
