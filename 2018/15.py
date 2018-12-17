from functools import total_ordering
import heapq

@total_ordering
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.occupant = None

    def has_unit(self):
        return self.occupant is not None and self.occupant.alive

    def is_near_enemies_of(self, race):
        return any(node.has_unit() and node.occupant.race != race for node in self.neighbours)

    def __repr__(self):
        return f'Node@{(self.x, self.y)}#{len(self.neighbours)}'
    
    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __eq__(self, other):
        return (self.y, self.x) == (other.y, other.x)
    
    def __hash__(self):
        return hash((self.x, self.y))

class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, new_node):
        for node in self.nodes:
            if self.distance(node, new_node) == 1:
                node.neighbours.append(new_node)
                new_node.neighbours.append(node)
        self.nodes.append(new_node)

    @staticmethod
    def distance(node1, node2):
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    def __repr__(self):
        return str(self.nodes)


class CombatUnit:
    def __init__(self, unit_id, race, node, attack_power):
        self.unit_id = unit_id
        self.race = race
        self.position = node
        self.hp = 200
        self.attack_power = attack_power

    @property
    def alive(self):
        return self.hp > 0

    @property
    def enemies_around(self):
        return [neighbour.occupant
                for neighbour in self.position.neighbours
                if neighbour.occupant is not None and neighbour.occupant.race != self.race]

    def perform_turn(self, units):
        if not self.alive:
            return False
        moved = False
        if not self.enemies_around:
            enemy_units = [unit for unit in units if unit.race != self.race]
            candidate_enemy_units = [unit for unit in enemy_units if len(unit.enemies_around) < len(unit.position.neighbours)]
            if candidate_enemy_units:
                moved = self.move()
        if self.enemies_around:
            self.attack()
        return moved
        
    def attack(self):
        opponent = min(self.enemies_around, key=lambda e: (e.hp, e.position.y, e.position.x))
        opponent.remove_hp(self.attack_power)

    def dprint(self, msg):
        return
        if self.unit_id == 10:
            print(f'[{self.unit_id}] - {msg}')

    def move(self):
        first_step = self._get_next_position()
        if first_step:
            self.position.occupant = None
            self.position = first_step
            self.position.occupant = self
            return True
        else:
            return False

    @staticmethod
    def _is_visited(node, visited, current_distance):
        return node in visited and visited[node] <= current_distance

    def _get_opponents_in_range(self):
        opponents = []
        visited = {}
        to_visit = []

        for neighbour in self.position.neighbours:
            if neighbour.occupant is None:
                if neighbour.is_near_enemies_of(self.race):
                    self.dprint(f' - Node {neighbour} is in range of an enemy. Adding to targets locations.')
                    opponents.append((neighbour, 2, neighbour))
                else:
                    heapq.heappush(to_visit, (1, neighbour, neighbour))

        while len(to_visit):
            distance, base_node, first_step = heapq.heappop(to_visit)

            # Some premature optimization :)
            if opponents and distance > min(opponents, key=lambda x: x[1])[1]:
                #self.dprint(f'Skipping node {base_node} because too far')
                continue

            # Skip a node if it has alrady been visited
            if self._is_visited(base_node, visited, distance):
                #self.dprint(f'Skipping node {base_node} because already visited')
                continue
            
            self.dprint(f'Analyzing node {base_node} with distance {distance}')
            visited[base_node] = distance
            for neighbour in base_node.neighbours:
                if neighbour.has_unit():
                    if neighbour.occupant.race == self.race:
                        # self.dprint(f' - NOT adding node {neighbour} because already occupied by {neighbour.occupant}')
                        continue
                elif self._is_visited(neighbour, visited, distance+1):
                    # self.dprint(f' - NOT adding node {neighbour} because already present (existing: {visited[neighbour]}; new: {distance})')
                    continue
                elif neighbour.is_near_enemies_of(self.race):
                    self.dprint(f' - Node {neighbour} is in range of an enemy. Adding to targets locations.')
                    opponents.append((neighbour, distance+1, first_step))
                    continue
                self.dprint(f' - Adding node {neighbour} with distance {distance+1}')
                heapq.heappush(to_visit, (distance+1, neighbour, first_step))
        return opponents

    def _get_next_position(self):
        opponents = self._get_opponents_in_range()
        if not opponents:
            return None # All enemy units must have been closed, so we cannot do much
        assert len(opponents)>0
        min_distance = min(opponents, key=lambda x: x[1])[1]
        nearest_opponents = [opponent for opponent in opponents if opponent[1]==min_distance]
        assert len(nearest_opponents)>0
        chosen_target = min(nearest_opponents, key=lambda x: x[0])
        first_step = chosen_target[2]
        self.dprint(f'There are {len(nearest_opponents)} at minimum distance {min_distance}')
        self.dprint(f'They are: {nearest_opponents}')
        self.dprint(f'The first calculated step is {first_step}')
        return first_step

    def remove_hp(self, attack_power):
        self.hp -= attack_power
        if not self.alive:
            self.position.occupant = None

    def __repr__(self):
        return f'{self.race}#{self.unit_id}@{(self.position.x, self.position.y)} ({"alive" if self.alive else "dead"}/{self.hp})'

def parse(data, elf_attack_power, goblin_attack_power):
    graph = Graph()
    units = []
    elves = []
    goblins = []
    unit_id = 0
    for y, line in enumerate(data):
        for x, cell in enumerate(line):
            if cell in '.EG':
                node = Node(x, y)
                graph.add_node(node)
            if cell == 'E':
                elf = CombatUnit(unit_id, 'Elf', node, elf_attack_power)
                unit_id += 1
                node.occupant = elf
                units.append(elf)
                elves.append(elf)
            elif cell == 'G':
                goblin = CombatUnit(unit_id, 'Goblin', node, goblin_attack_power)
                unit_id += 1
                units.append(goblin)
                node.occupant = goblin
                goblins.append(goblin)
    return graph, units, elves, goblins, x

def print_state(size, graph, units):
    table = [
        ['#' for _x in range(size+1)]
        for _y in range(size+1)
    ]
    for node in graph.nodes:
        table[node.y][node.x] = '.'
    for unit in units:
        if unit.alive:
            table[unit.position.y][unit.position.x] = unit.race[0] # str(hex(unit.unit_id))[-1:]
    lines = ['  0123456789012345678901234567890']
    for i, line in enumerate(table):
        lines.append(str(i).rjust(2) + ''.join(c for c in line))
    res = '\n'.join(lines)
    print(res)


def fight_for_chocolate(elf_attack_power):
    graph, units, elves, goblins, size = parse(data, elf_attack_power=elf_attack_power, goblin_attack_power=3)
    current_turn = 0
    while any(elf.alive for elf in elves) and any(goblin.alive for goblin in goblins):
        current_turn += 1
        units = sorted(units, key=lambda u:u.position)
        any_moved = False
        for unit in units:
            any_moved = unit.perform_turn(units) or any_moved
        # print_state(size, graph, units)
    return current_turn-1, units, elves, goblins


data = open('input_15.txt').readlines()
data = [line.split(' ')[0] for line in data]
data = [line.strip('\n') for line in data]

last_full_turn, units, elves, goblins = fight_for_chocolate(3)
total_hit_points = sum(u.hp for u in units if u.alive)

print(f'Combat ends after {last_full_turn} full rounds')
if any(elf.alive for elf in elves):
    print(f'Elves win with {total_hit_points} total hit points left')
else:
    print(f'Goblins win with {total_hit_points} total hit points left')
print(f'Outcome: {last_full_turn} * {total_hit_points} = {last_full_turn*total_hit_points}')


#######################

low_attack_power = 3
high_attack_power = 200

while high_attack_power-low_attack_power > 1:
    current_attack_power = (high_attack_power + low_attack_power) // 2
    last_full_turn, units, elves, goblins = fight_for_chocolate(current_attack_power)
    elves_alive = [elf for elf in elves if elf.alive]
    survival_rate = len(elves_alive) / len(elves)
    print(f'Elf attack set to {current_attack_power} lead to {survival_rate:03.2%} survival rate')
    if survival_rate==1:
        high_attack_power = current_attack_power
    else:
        low_attack_power = current_attack_power

print(f"Lowest possible attack power for elves to win is {high_attack_power}")


last_full_turn, units, elves, goblins = fight_for_chocolate(23)
total_hit_points = sum(u.hp for u in units if u.alive)

print(f'Combat ends after {last_full_turn} full rounds')
if any(elf.alive for elf in elves):
    print(f'Elves win with {total_hit_points} total hit points left')
else:
    print(f'Goblins win with {total_hit_points} total hit points left')
print(f'Outcome: {last_full_turn} * {total_hit_points} = {last_full_turn*total_hit_points}')
