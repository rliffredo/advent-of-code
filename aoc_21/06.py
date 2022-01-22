from collections import Counter

from common import read_data


def parse_data():
    raw_data = read_data("06", False)
    input_population = [int(n) for n in raw_data.split(",")]
    first_generation = Counter(input_population)
    return {**{n: 0 for n in range(9)}, **first_generation}


def reproduce(current_population):
    reproducing_fishes = current_population[0]
    new_population = {}
    for n in range(8):
        new_population[n] = current_population[n + 1]
    new_population[8] = reproducing_fishes
    new_population[6] += reproducing_fishes
    return new_population


def count_population(current_population):
    return sum(current_population.values())


def part_1(print_result: bool = True) -> int:
    current_population = parse_data()
    for n in range(80):
        current_population = reproduce(current_population)
    return count_population(current_population)


def part_2(print_result: bool = True) -> int:
    current_population = parse_data()
    for n in range(256):
        current_population = reproduce(current_population)
    return count_population(current_population)


SOLUTION_1 = 360268
SOLUTION_2 = 1632146183902

if __name__ == "__main__":
    print(part_1())
    print(part_2())
