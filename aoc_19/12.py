import itertools
from dataclasses import dataclass
from typing import List

from math import gcd
from functools import reduce


@dataclass
class Moon:
    name: str
    pos: List[int]
    speed: List[int]

    @property
    def pot(self):
        return sum(map(abs, self.pos))

    @property
    def kin(self):
        return sum(map(abs, self.speed))

    @property
    def total(self):
        return self.pot * self.kin

    def axis_state(self, axis):
        return self.pos[axis], self.speed[axis]


def load_initial_state():
    return [
               Moon(name='Io', pos=[6, -2, -7], speed=[0, 0, 0]),
               Moon(name='Europa', pos=[-6, -7, -4], speed=[0, 0, 0]),
               Moon(name='Ganymede', pos=[-9, 11, 0], speed=[0, 0, 0]),
               Moon(name='Callisto', pos=[-3, -4, 6], speed=[0, 0, 0]),
           ], 1000


def load_initial_state_test_1():
    return [
               Moon(name='Io', pos=[-1, 0, 2], speed=[0, 0, 0]),
               Moon(name='Europa', pos=[2, -10, -7], speed=[0, 0, 0]),
               Moon(name='Ganymede', pos=[4, -8, 8], speed=[0, 0, 0]),
               Moon(name='Callisto', pos=[3, 5, -1], speed=[0, 0, 0]),
           ], 10


def load_initial_state_test_2():
    return [
               Moon(name='Io', pos=[-8, -10, 0], speed=[0, 0, 0]),
               Moon(name='Europa', pos=[5, 5, 10], speed=[0, 0, 0]),
               Moon(name='Ganymede', pos=[2, -7, 3], speed=[0, 0, 0]),
               Moon(name='Callisto', pos=[9, -8, -3], speed=[0, 0, 0]),
           ], 100


def accelerate_moon(moon, other):
    for coord in [0, 1, 2]:
        acceleration = 1 if moon.pos[coord] < other.pos[coord] else -1 if moon.pos[coord] > other.pos[coord] else 0
        moon.speed[coord] += acceleration


def move_moon(moon):
    for coord in [0, 1, 2]:
        moon.pos[coord] += moon.speed[coord]


def apply_gravity(moons):
    for moon_pair in itertools.permutations(moons, 2):
        accelerate_moon(*moon_pair)


def apply_speed(moons):
    for moon in moons:
        move_moon(moon)


def calculate_energy(moons):
    pot = sum(map(lambda m: m.pot, moons))
    kin = sum(map(lambda m: m.kin, moons))
    total = sum(map(lambda m: m.total, moons))
    return pot, kin, total


def print_state(iteration, moons, pot, kin, total):
    print(f'*** Iteration {iteration}: pot={pot}, kin={kin}; total={total} ***')
    for moon in moons:
        print(f'{moon.name} pos={moon.pos}, vel={moon.speed}')


################
# ## PART 1 ## #
################

def calculate_energy_after_positions(moons, max_iterations):
    # print_state(0, moons, *calculate_energy(moons))
    energies = [0, 0, 0]
    for n in range(max_iterations):
        apply_gravity(moons)
        apply_speed(moons)
        energies = calculate_energy(moons)
        # print_state(n + 1, moons, *energies)
    return energies[2]


moon_state, amount = load_initial_state()
# moons, amount = load_initial_state_test_1()
# moons, amount = load_initial_state_test_2()
print(f'Total energy after {amount} steps: {calculate_energy_after_positions(moon_state, amount)}')  # 7098


################
# ## PART 2 ## #
################
def find_axis_cycle(moons, states, axis):
    new_state = tuple(moon.axis_state(axis) for moon in moons)
    if new_state in states:
        # print(f'Found cycle for axis {axis}: {len(states)}')
        return len(states)
    else:
        states.add(new_state)
        return 0


def get_cycle_lengths(moons):
    states = [set(), set(), set()]
    for axis in [0, 1, 2]:
        find_axis_cycle(moons, states[axis], axis)
    cycle_length = [0, 0, 0]
    while True:
        apply_gravity(moons)
        apply_speed(moons)
        for axis in [0, 1, 2]:
            if not cycle_length[axis]:
                cycle_length[axis] = find_axis_cycle(moons, states[axis], axis)
        if all(cycle_length):
            return cycle_length


def lcm(numbers):
    return reduce(lambda a, b: a * b // gcd(a, b), numbers)


def get_system_cycle(moons):
    cycles = get_cycle_lengths(moons)
    return lcm(cycles)


# moon_state, _ = load_initial_state_test_1()
# moon_state, _ = load_initial_state_test_2()
moon_state, _ = load_initial_state()
print(f'Steps for repeating state: {get_system_cycle(moon_state)}')  # 400128139852752
