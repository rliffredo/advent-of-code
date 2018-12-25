import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Group:
    group_id: int
    system: str
    units: int
    hit_points: int
    attack_damage: int
    attack_type: str
    initiative: int
    weaknesses: List[str]
    immunities: List[str]
    target: Optional['Group']
    target_of: Optional['Group']

    @property
    def alive(self) -> bool:
        return self.units > 0

    @property
    def effective_power(self) -> int:
        return self.units * self.attack_damage if self.alive else 0

    def select_target(self, all_groups: List['Group']) -> None:
        def priority_criteria(g: Group):
            return -g.eval_damage(self.effective_power, self.attack_type), -g.effective_power, -g.initiative

        self.target = None
        candidates = [g for g in all_groups if g.system != self.system and g.alive and g.target_of is None]
        if not candidates:
            return
        prioritized_candidates = sorted(candidates, key=priority_criteria)
        # for candidate in prioritized_candidates:
        #     print(f' - {self} evaluated {candidate} and would cause {candidate.eval_damage(self.effective_power, self.attack_type)}')
        target = prioritized_candidates[0]
        if target.eval_damage(self.effective_power, self.attack_type) == 0:
            return
        # print(f'{self} will attack {target}')
        self.target = target
        target.target_of = self

    def eval_damage(self, amount: int, damage_type: str) -> int:
        if damage_type in self.immunities:
            return 0
        elif damage_type in self.weaknesses:
            return amount * 2
        else:
            return amount

    def damage(self, amount: int, damage_type: str) -> int:
        damage = self.eval_damage(amount, damage_type)
        killed_units = damage // self.hit_points
        # if killed_units > 0:
        #     print(f'{self.target_of} hit {self} with {damage}, and {killed_units} units were lost')
        self.units -= killed_units
        # if not self.alive:
        #     print(f' - {self} was killed by {self.target_of}!')
        return killed_units

    def attack(self) -> int:
        if not self.target:
            return 0
        killed_units = 0
        if self.target.alive:
            killed_units = self.target.damage(self.effective_power, self.attack_type)
        self.target.target_of = None
        self.target = None
        return killed_units

    def __str__(self):
        return f'{self.system[:3]}:{self.group_id}/{self.units}/{self.effective_power}'


def parse_line(line: str, system: str, group_id: int, boost: int):
    # 17 units each with 5390 hit points (immune to fire; weak to bludgeoning, slashing)
    #  with an attack that does 4507 fire damage at initiative 2
    m = re.match(r'(\d+) units each with (\d+) hit points (\(.*\) )?with an attack that '
                 r'does (\d+) ([a-z]+) damage at initiative (\d+)', line)
    assert m is not None, f'*** Could not parse line {line} because not according to pattern'
    mg = m.groups()
    immunities = []
    weaknesses = []
    if mg[2]:
        # (immune to fire; weak to bludgeoning, slashing)
        line = mg[2].strip('() ')
        for sub_line in line.split('; '):
            kind, types = sub_line.split('to ')
            if kind.strip() == 'immune':
                immunities = types.split(', ')
            else:
                weaknesses = types.split(', ')

    return Group(
        group_id=group_id,
        system=system,
        units=int(mg[0]),
        hit_points=int(mg[1]),
        attack_damage=int(mg[3]) + (boost if system =='Immune System' else 0),
        attack_type=mg[4],
        initiative=int(mg[5]),
        weaknesses=weaknesses,
        immunities=immunities,
        target=None,
        target_of=None)


def parse_file(boost: int) -> List[Group]:
    data = open('input_24.txt').readlines()
    all_units: List[Group] = []
    current_system = None
    current_group_id = 0
    for line in data:
        line = line.strip()
        if not line:
            continue
        elif line.endswith(':'):
            current_system = line.strip(':')
            current_group_id = 1
        else:
            assert current_system is not None
            group = parse_line(line, current_system, current_group_id, boost)
            # print(f'Added group {group} with '
            #       f'{",".join(group.weaknesses)} weaknesses and {",".join(group.immunities)} immunities')
            all_units.append(group)
            current_group_id += 1
    return all_units


def target_phase_order(all_groups: List[Group]):
    def priority_criteria(g: Group):
        return -g.effective_power, -g.initiative

    return sorted(all_groups, key=priority_criteria)


def attack_phase_order(all_groups: List[Group]):
    def priority_criteria(g: Group):
        return -g.initiative

    return sorted(all_groups, key=priority_criteria)


def winner(all_groups: List[Group]) -> Optional[str]:
    counter = defaultdict(int)
    for group in all_groups:
        if group.alive:
            counter[group.system] += 1
    teams_alive = list(counter.keys())
    assert len(teams_alive) > 0, 'At least one team must be still alive!'
    return teams_alive[0] if len(teams_alive) == 1 else None


def calc_winner(boost=0):
    groups = parse_file(boost)

    print('Initial situation')
    for group in groups:
        print(f' - {group}')

    stalemate = 0
    current_round = 0
    while winner(groups) is None:
        if current_round % 1 == 0:
            immune = sum(group.units for group in groups if group.system == 'Immune System')
            infection = sum(group.units for group in groups if group.system == 'Infection')
            # print(f'*** Round {current_round}: {immune} units left for immune system, '
            #       f'and {infection} units left for infection ***')
        for group in target_phase_order(groups):
            group.select_target(groups)
        total_killed = 0
        for group in attack_phase_order(groups):
            total_killed += group.attack()
        if total_killed == 0:
            stalemate += 1
        else:
            stalemate = 0
        if stalemate > 3:
            print(f'Reached a stalemate at round {current_round}')
            return "None", 0
        current_round += 1

    units = sum(group.units for group in groups if group.alive)

    print(f' Winner is {winner(groups)} with {units} units (boost to immune system: {boost})')
    print('Final situation')
    for group in groups:
        print(f' - {group}')

    return winner(groups), units


calc_winner(0)


boost = 1
while True:
    winner_side, units = calc_winner(boost)
    if winner_side == 'Immune System':
        print(f'Minimum boost is: {boost}')
        break
    boost += 1
