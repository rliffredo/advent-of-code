import math


def read_data(filename):
    f = open(filename)
    modules = f.readlines()
    return [int(m) for m in modules]


mods = read_data('data/01.txt')


def fuel_for_module(m):
    return math.floor(m / 3) - 2


answer_1 = sum(fuel_for_module(m) for m in mods)  # 3233481
print(f'Required fuel for spaceship: {answer_1}')

#########


def additional_fuel(additional_mass):
    fuel = 0
    while additional_mass >= 0:
        required_fuel = fuel_for_module(additional_mass)
        if required_fuel >= 0:
            fuel += required_fuel
        additional_mass = required_fuel
    return fuel


def get_corrected_fuel(m):
    f = fuel_for_module(m)
    c = additional_fuel(f)
    return c + f


answer_2 = sum(get_corrected_fuel(m) for m in mods)  # 4847351
print(f'Required fuel for spaceship (fixed): {answer_2}')
