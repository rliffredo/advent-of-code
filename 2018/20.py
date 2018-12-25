import heapq
from collections import namedtuple
from dataclasses import dataclass
from typing import Dict, List, Set


Coords = namedtuple('Coords', 'x, y')

BASE_ROOM_COORDS = Coords(100, 100)


@dataclass
class Room:
    coords: Coords
    neighbours: Dict[str, 'Room']

    def __repr__(self):
        return f'Room@{self.coords}/{"".join(self.neighbours.keys())}'


def move(current_place: Coords, direction) -> Coords:
    if direction == 'N':
        return Coords(current_place.x, current_place.y-1)
    elif direction == 'S':
        return Coords(current_place.x, current_place.y+1)
    elif direction == 'W':
        return Coords(current_place.x-1, current_place.y)
    elif direction == 'E':
        return Coords(current_place.x+1, current_place.y)


inverse_dir = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


def parse_regex(line: str, palace_map: Dict[Coords, Room]):
    start_room = palace_map[BASE_ROOM_COORDS]
    line = list(reversed(line))
    parse_regex_token(line, palace_map, start_room)


def parse_regex_token(line, palace_map, start_room):
    current_room = start_room
    while line:
        direction = line.pop()
        if direction == '^':
            current_room = start_room
        if direction in 'NSWE':
            new_coords = move(current_room.coords, direction)
            if new_coords not in palace_map:
                palace_map[new_coords] = Room(new_coords, {})
            new_room = palace_map[new_coords]
            current_room.neighbours[direction] = new_room
            new_room.neighbours[inverse_dir[direction]] = current_room
            current_room = new_room
        if direction == '(':
            parse_regex_token(line, palace_map, current_room)
        if direction == ')':
            return
        if direction == '|':
            current_room = start_room


def read_data() -> Dict[Coords, Room]:
    data = open('input_20.txt').readlines()
    data = [line.strip('\n') for line in data]
    palace_map = {BASE_ROOM_COORDS: Room(BASE_ROOM_COORDS, {})}
    for line in data:
        if line:
            parse_regex(line, palace_map)
    return palace_map


def print_palace(palace_map: Dict[Coords, Room]):
    min_x = min(c.x for c in palace_map)
    min_y = min(c.y for c in palace_map)
    max_x = max(c.x for c in palace_map)
    max_y = max(c.y for c in palace_map)

    # Draw all walls
    width = (max_x-min_x+1)*2 + 1
    height = (max_y-min_y+1)*2 + 1
    table = [
        ['#' for _x in range(width)]
        for _y in range(height)
    ]

    # Draw rooms and doors
    for room_position in palace_map:
        x = (room_position.x - min_x) * 2 + 1
        y = (room_position.y - min_y) * 2 + 1
        assert 0 < y <= height
        assert 0 < x <= width
        table[y][x] = '.'
        doors = [direction for direction in palace_map[room_position].neighbours]
        for door in doors:
            if door == 'N':
                table[y-1][x] = '-'
            if door == 'S':
                table[y+1][x] = '-'
            if door == 'W':
                table[y][x-1] = '|'
            if door == 'E':
                table[y][x+1] = '|'

    # Draw base
    x = (100 - min_x) * 2 + 1
    y = (100 - min_y) * 2 + 1
    table[y][x] = 'X'

    # Paint
    lines = []
    for i, line in enumerate(table):
        lines.append(''.join(c for c in line))
    res = '\n'.join(lines) + '\n'
    print(res)


@dataclass
class QueueElement:
    room: Room
    path: str

    @property
    def path_len(self):
        if not hasattr(self, '_path_len'):
            setattr(self, '_path_len', len(self.path))
        return getattr(self, '_path_len')

    def __lt__(self, other: 'QueueElement'):
        return self.path_len < self.path_len

    def __eq__(self, other: 'QueueElement'):
        return self.path_len == self.path_len


def assign_distance_to_rooms(base_room: Room) -> Dict[Coords, int]:
    rooms_visited: Dict[Coords, int] = {}
    rooms_to_visit: List[QueueElement] = []
    heapq.heappush(rooms_to_visit, QueueElement(base_room, ''))
    while len(rooms_to_visit) > 0:
        current_room = heapq.heappop(rooms_to_visit)  # type: QueueElement
        rooms_visited[current_room.room.coords] = current_room.path_len
        for direction, neighbour in current_room.room.neighbours.items():
            if neighbour.coords in rooms_visited:
                continue
            node_to_visit = QueueElement(neighbour, current_room.path + direction)
            heapq.heappush(rooms_to_visit, node_to_visit)
    return rooms_visited


def distance_to_farthest_room(palace_map: Dict[Coords, Room]) -> int:
    base_room = palace_map[BASE_ROOM_COORDS]
    room_distances = assign_distance_to_rooms(base_room)
    most_distant = max(room_distances.items(), key=lambda rd: rd[1])
    return most_distant[1]


palace = read_data()
print_palace(palace)

print(f'In the palace the farthest room is {distance_to_farthest_room(palace)} doors distant')

#########


def rooms_farther_than(palace_map: Dict[Coords, Room], min_distance) -> int:
    base_room = palace_map[BASE_ROOM_COORDS]
    room_distances = assign_distance_to_rooms(base_room)
    distant_rooms = [room for room in room_distances if room_distances[room] >= min_distance]
    return len(distant_rooms)


print(f'In the palace the number of rooms farther than 1000 doors is {rooms_farther_than(palace, 1000)}')
