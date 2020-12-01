import itertools
import re

from common import read_data, intcode


class ZorkDroid:

    def __init__(self):
        self.computer = intcode.IntCode(self.provide_input, self.collect_output)
        self.computer.load(read_data("25"))
        self.description = []
        self.user_input = TO_SECURITY
        self.current_room = ''
        self.current_items = set(ALL_ITEMS)
        self.weight_state = ''

        self.weight_combinations = itertools.chain(
            itertools.combinations(ALL_ITEMS, 3),
            itertools.combinations(ALL_ITEMS, 4),
            itertools.combinations(ALL_ITEMS, 5),
            itertools.combinations(ALL_ITEMS, 6),
            itertools.combinations(ALL_ITEMS, 7),
            itertools.combinations(ALL_ITEMS, 8),
        )

    def run(self):
        self.computer.execute()

    def collect_output(self, value):
        if value == 10:
            description = ''.join(self.description)
            self.check_room_name(description)
            self.check_permission(description)
            print(description)
            self.description.clear()
        else:
            self.description.append(chr(value))

    def check_permission(self, description):
        response_match = re.match(r'.*Droids on this ship are ([a-z]*).*', description)
        if response_match:
            self.weight_state = response_match.groups()[0]

    def check_room_name(self, description):
        name_match = re.match('==([^=]+)==', description)
        if name_match:
            self.current_room = name_match.groups()[0].strip()

    def provide_input(self):
        if not self.user_input:
            if self.current_room == 'Security Checkpoint':
                self.try_combinations()
            else:
                self.user_input = input() + '\n'
        char = self.user_input[0]
        self.user_input = self.user_input[1:]
        return ord(char)

    def try_combinations(self):
        new_combination = set(next(self.weight_combinations))
        items_to_drop = self.current_items - new_combination
        items_to_take = new_combination - self.current_items
        self.current_items = new_combination
        commands = [f'drop {it}' for it in items_to_drop] + [f'take {it}' for it in items_to_take]
        self.user_input = '\n'.join(commands) + '\nwest\n'


TO_SECURITY = """south
west
west
take easter egg
east
take fuel cell
east
north
north
north
east
east
take cake
west
west
south
south
east
take ornament
east
take hologram
east
take dark matter
north
north
east
take klein bottle
north
take hypercube
north
west
"""

ALL_ITEMS = [
    "ornament",
    "easter egg",
    "hypercube",
    "hologram",
    "cake",
    "fuel cell",
    "dark matter",
    "klein bottle",
]

zd = ZorkDroid()
zd.run()

