from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple

import networkx as nx

from common import read_data, intcode, print_map, get_map_dimensions


class Direction(IntEnum):
    N = 1
    S = 2
    W = 3
    E = 4

    @staticmethod
    def directions():
        return Direction.N, Direction.S, Direction.W, Direction.E

    def opposite(self) -> 'Direction':
        return {
            Direction.N: Direction.S,
            Direction.S: Direction.N,
            Direction.E: Direction.W,
            Direction.W: Direction.E
        }[self]


def get_neighbour(position: Tuple[int, int], direction: Direction) -> Tuple[int, int]:
    new_x = position[0] + (1 if direction == Direction.E else -1 if direction == Direction.W else 0)
    new_y = position[1] + (1 if direction == Direction.S else -1 if direction == Direction.N else 0)
    return new_x, new_y


class SquareType(IntEnum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2


@dataclass
class ShipLocation:
    position: Tuple[int, int]
    status: SquareType


class ExitProgram(Exception):
    """
    Signal that program has exited
    """


class RepairerRobot:

    def __init__(self, mode_bot):
        self.ship_map = {(0, 0): ShipLocation(position=(0, 0), status=SquareType.EMPTY)}
        self.map_graph = nx.Graph()
        self.pos = (0, 0)
        self.dir = None
        self.computer = intcode.IntCode(input_provider=self.movement, output_provider=self.movement_feedback)
        self.computer.load(read_data("15"))
        self.oxygen = None
        self.mode_bot = mode_bot
        self.browser = self.browse_ship()

    def find_oxygen(self) -> bool:
        """
        Returns the minimum amount of steps to find the oxygen
        """
        try:
            self.computer.execute()
        except ExitProgram:
            pass
        if self.oxygen:
            return True
        else:
            return False

    def movement_feedback(self, value):
        feedback = SquareType(value)
        new_pos = get_neighbour(self.pos, self.dir)
        if new_pos not in self.ship_map:
            self.ship_map[new_pos] = ShipLocation(status=feedback, position=new_pos)
        else:
            assert self.ship_map[new_pos].status == feedback, "Status is consistent from any direction"

        if feedback != SquareType.WALL:
            self.map_graph.add_edge(self.pos, new_pos)
            self.pos = new_pos

        if feedback == SquareType.OXYGEN:
            self.oxygen = new_pos

    def movement(self):
        self.dir = self.bot_input() if self.mode_bot else self.user_input()
        return self.dir.value

    def user_input(self):
        print('Current map')
        dimensions = get_map_dimensions(self.ship_map)
        print_map(dimensions, self.map_meaning)
        user_input = int(input('Movement? [north (1), south (2), west (3), east (4), or anything else to exit] > '))
        if not 1 <= user_input <= 4:
            raise ExitProgram()
        return Direction(user_input)

    def map_meaning(self, x: int, y: int) -> str:
        position = (x, y)
        if position == self.pos:
            return 'R'
        if position not in self.ship_map:
            return '?'
        if self.ship_map[position].status == SquareType.EMPTY:
            return ' '
        if self.ship_map[position].status == SquareType.WALL:
            return '#'
        if self.ship_map[position].status == SquareType.OXYGEN:
            return 'O'
        assert False, 'All possible cases for the maps have been taken into consideration'

    def bot_input(self):
        try:
            return next(self.browser)
        except StopIteration:
            raise ExitProgram()

    def browse_ship(self):
        return self.visit_node((0, 0))

    def visit_node(self, node: Tuple[int, int]):
        assert self.pos == node
        neighbours = {get_neighbour(node, d): d for d in Direction.directions()}
        for neighbour in neighbours:
            if neighbour in self.ship_map:
                continue
            movement = neighbours[neighbour]
            yield movement
            assert neighbour in self.ship_map
            if self.ship_map[neighbour].status != SquareType.WALL:
                assert self.pos == neighbour
                yield from self.visit_node(neighbour)
                yield movement.opposite()  # we visited all neighbours, go back


################
# ## PART 1 ## #
################

robot = RepairerRobot(mode_bot=True)
found = robot.find_oxygen()

print("*** Ship map ***")
print_map(get_map_dimensions(robot.ship_map), robot.map_meaning)

steps = nx.shortest_path_length(robot.map_graph, (0, 0), robot.oxygen)
print(f'Number of steps to move to the oxygen: {steps}')  # 234

################
# ## PART 2 ## #
################

minutes = max(nx.shortest_path_length(robot.map_graph, p, robot.oxygen) for p in robot.map_graph.nodes)
print(f'Number of minutes to fill with oxygen: {minutes}')  # 292
