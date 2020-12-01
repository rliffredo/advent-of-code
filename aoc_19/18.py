import heapq
import string
from itertools import chain
from typing import Tuple, Sequence, Dict, Set, Callable

import networkx as nx

from common import read_data

Point = Tuple[int, int]
NodePoint = Tuple[Point, Dict[str, str]]

ROOTS = {'@', '%', '*', '&'}


def neighbours(point: Point) -> Sequence[Point]:
    x = point[0]
    y = point[1]
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


class FloorMap:
    distance_cache: Dict[Tuple[str, str], int] = {}

    def __init__(self, map_lines: Sequence[str]):
        """
        General map with nodes and items
        """

        self.fm = nx.Graph()
        for y, line in enumerate(map_lines):
            for x, ch in enumerate(line.strip()):
                if ch == '#':
                    continue

                # Add edges to the neighbours
                for n in neighbours((x, y)):
                    if map_lines[n[1]][n[0]] != '#':
                        self.fm.add_edge((x, y), n)

                # Add key information
                if ch == '.':
                    self.fm.nodes[(x, y)]['type'] = 'passage'
                    self.fm.nodes[(x, y)]['item'] = 'none'
                else:
                    self.fm.nodes[(x, y)][
                        'type'] = 'root' if ch in ROOTS else 'door' if ch in string.ascii_uppercase else 'key'
                    self.fm.nodes[(x, y)]['item'] = ch.lower()

    def get_item_coordinates(self, key_name: str) -> Point:
        return next(n[0]
                    for n in chain(self.get_all_keys(), self.get_all_roots())
                    if n[1]["item"] == key_name.lower())

    def get_all_roots(self) -> Sequence[NodePoint]:
        return [n for n in self.fm.nodes(data=True) if n[1]["type"] == "root"]

    def get_all_keys(self) -> Sequence[NodePoint]:
        return [n for n in self.fm.nodes(data=True) if n[1]["type"] == "key"]

    def get_all_doors(self) -> Sequence[NodePoint]:
        return [n for n in self.fm.nodes(data=True) if n[1]["type"] == "door"]

    def get_key_dependencies(self, start_name: str,
                             floor_keys: Sequence[NodePoint]) -> Dict[str, Sequence[NodePoint]]:
        def doors_for_key(start_coords: Tuple[int, int], key_position: Tuple[int, int]):
            """
            Returns a list with all doors required to get a certain key
            """
            blocking_doors = []
            for door in self.get_all_doors():
                door_pos = door[0]
                if door_pos not in list(self.fm.nodes):
                    continue
                plan = self.fm.copy()
                plan.remove_node(door_pos)
                if not nx.has_path(plan, start_coords, key_position):
                    blocking_doors.append(door[1]['item'])
            return blocking_doors

        start_position = self.get_item_coordinates(start_name)
        key_dependencies = {key[1]["item"]: doors_for_key(start_position, key[0])
                            for key in floor_keys}

        return key_dependencies

    def calc_distance(self, from_key: str, to_key: str) -> int:
        """
        Calculate distance between two keys, caching it for better performance.
        """
        if (from_key, to_key) not in self.distance_cache:
            from_coord = self.get_item_coordinates(from_key)
            to_coord = self.get_item_coordinates(to_key)
            self.distance_cache[(from_key, to_key)] = nx.shortest_path_length(self.fm, from_coord, to_coord)
        return self.distance_cache[(from_key, to_key)]


class StepsQueue:
    def __init__(self):
        self.queue = []
        self.last_pick = 0

    def push(self, bot_positions: Dict[str, str], total_distance: int, collected_keys: str) -> None:
        heapq.heappush(self.queue, (0, total_distance, collected_keys, bot_positions.items()))

    def pop(self) -> Tuple[Dict[str, str], int, str]:
        self.last_pick, total_distance, collected_keys, bot_positions = heapq.heappop(self.queue)
        return {k: v for k, v in bot_positions}, total_distance, collected_keys

    def is_empty(self):
        return len(self.queue) == 0

    def __len__(self):
        return len(self.queue)


def get_accessible_keys(collected_keys: str, key_dependencies: Dict[str, Sequence[NodePoint]]) -> Set[str]:
    opened_doors = {k for k in collected_keys}
    accessible_keys = {k for k, v in key_dependencies.items() if len(set(v) - opened_doors) == 0}
    keys_to_analyze = accessible_keys - opened_doors
    return keys_to_analyze


def get_accessible_keys_in_sector(sector_name: str, collected_keys: str,
                                  key_dependencies: Dict[str, Dict[str, Sequence[NodePoint]]]) -> Set[str]:
    return get_accessible_keys(collected_keys, key_dependencies[sector_name])


def calculate_shortest_path(map_lines: Sequence[str],
                            map_splitter: Callable[[FloorMap], None],
                            key_splitter: Callable[[FloorMap], Dict[str, Sequence[NodePoint]]]) -> Tuple[int, str]:
    print("Making floor map...")
    floor_map = FloorMap(map_lines)
    map_splitter(floor_map)
    sector_keys = key_splitter(floor_map)
    print("Calculating key dependencies...")
    key_dependencies = {sector_key_name: floor_map.get_key_dependencies(sector_key_name, keys_ins_sector)
                        for sector_key_name, keys_ins_sector in sector_keys.items()}
    total_keys = sum(len(deps) for deps in key_dependencies.values())

    nodes = {}
    q = StepsQueue()

    print("Finding shortest path covering all keys...")
    sectors_entrances = {sector_key[1]["item"]: sector_key[1]["item"] for sector_key in floor_map.get_all_roots()}
    q.push(sectors_entrances, 0, '')
    max_dist = -1
    max_collected_keys = ''
    while not q.is_empty():
        bot_positions, dist_so_far, collected_keys = q.pop()
        if dist_so_far > max_dist:
            max_dist = dist_so_far
        if len(collected_keys) > len(max_collected_keys):
            max_collected_keys = collected_keys
        if len(collected_keys) == total_keys:
            break
        for sector_name, key_name in bot_positions.items():
            keys = get_accessible_keys_in_sector(sector_name, collected_keys, key_dependencies)
            if not keys:
                continue
            for key in keys:
                distance = floor_map.calc_distance(key_name, key)
                steps_to_node = dist_so_far + distance
                keys_for_location = collected_keys + key

                node_and_keys = (key, tuple(sorted(keys_for_location)))
                if node_and_keys not in nodes:
                    nodes[node_and_keys] = steps_to_node
                elif nodes[node_and_keys] > steps_to_node:
                    nodes[node_and_keys] = steps_to_node
                else:
                    continue
                next_bp = bot_positions.copy()
                next_bp[sector_name] = key
                q.push(next_bp, steps_to_node, keys_for_location)

    return max_dist, max_collected_keys


################
# ## PART 1 ## #
################

string_data = read_data("18", by_lines=True)
steps, shortest_path = calculate_shortest_path(string_data, lambda _: None, lambda fm: {'@': fm.get_all_keys()})
print(f'Minimum amount of steps to collect all keys is {steps}, for path {shortest_path}')  # 4250


################
# ## PART 2 ## #
################

def split_floor_map(floor_map: FloorMap) -> None:
    key_x, key_y = floor_map.get_item_coordinates('@')
    # Remove nodes that now are walls
    for node in [(key_x, key_y), (key_x - 1, key_y), (key_x + 1, key_y), (key_x, key_y - 1), (key_x, key_y + 1)]:
        assert node in floor_map.fm.nodes, 'Map is friendly ;-)'
        floor_map.fm.remove_node(node)
    # Add/alter nodes to host keys
    for root, node in zip(ROOTS, [(key_x - 1, key_y - 1), (key_x + 1, key_y - 1), (key_x - 1, key_y + 1),
                                  (key_x + 1, key_y + 1)]):
        assert node in floor_map.fm.nodes, 'Map is friendly ;-)'
        floor_map.fm.nodes[node]['type'] = 'root'
        floor_map.fm.nodes[node]['item'] = root


def split_keys_by_sector(floor_map: FloorMap) -> Dict[str, Sequence[NodePoint]]:
    keys_by_sector = {k: [] for k in ROOTS}
    entrance_coords = {key: floor_map.get_item_coordinates(key) for key in ROOTS}
    for key in floor_map.get_all_keys():
        key_coords = key[0]
        for sector_start in entrance_coords:
            if nx.has_path(floor_map.fm, entrance_coords[sector_start], key_coords):
                keys_by_sector[sector_start].append(key)
                break
        else:
            assert False, f'No path for {key}'
    return keys_by_sector


string_data = read_data("18", by_lines=True)
steps, shortest_path = calculate_shortest_path(string_data, split_floor_map, split_keys_by_sector)
print(f'Minimum amount of steps to collect all keys is {steps}, for path {shortest_path}')  # 1640
