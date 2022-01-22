from typing import Set, List

import networkx as nx

from common import read_data


def parse_data():
    raw_data = read_data("12", True)
    cave = nx.Graph()
    for line in raw_data:
        n1, n2 = line.split("-")
        cave.add_edge(n1, n2)
    return cave


def explore_room(rooms, all_rooms, room: str, visited_rooms: Set):
    neighbours = list(rooms[room])  # weird...
    for neighbour in neighbours:
        explore_room(rooms, all_rooms, neighbour, visited_rooms.copy())


def find_paths(cave, start, end, visited_rooms: str, visited_twice: str, visit_once: bool) -> List[str]:
    if start == end:
        return [visited_rooms]
    if start.islower() and start in visited_rooms:
        if visit_once:
            # part 1
            return []
        if visited_twice or start in ["start", "end"]:
            # part 2
            return []
        visited_twice = start
    visited_rooms += start
    paths = []
    # in NetworkX, a graph is a dictionary-like structure, where for each node you get the list (sequence, actually) of
    # all neighbours
    for neighbor in cave[start]:
        paths += find_paths(cave, neighbor, end, visited_rooms, visited_twice, visit_once)
    return paths


def part_1(print_result: bool = True) -> int:
    cave = parse_data()
    all_paths = find_paths(cave, "start", "end", "", "", True)
    return len(all_paths)


def part_2(print_result: bool = True) -> int:
    cave = parse_data()
    all_paths = find_paths(cave, "start", "end", "", "", False)
    return len(all_paths)


SOLUTION_1 = 4241
SOLUTION_2 = 122134

if __name__ == "__main__":
    print(part_1())
    print(part_2())
