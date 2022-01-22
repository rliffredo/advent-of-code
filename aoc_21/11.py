from common import read_data, print_map


def parse_data():
    raw_data = read_data("11", True)
    octopuses = {}
    for y, line in enumerate(raw_data):
        for x, c in enumerate(line):
            octopuses[x, y] = int(c)
    return octopuses


def flash(new_step, x, y):
    new_step[x, y] = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if 0 <= x+dx < 10 and 0 <= y+dy < 10 and not (dx == 0 and dy == 0):
                if new_step[x+dx, y+dy] != 0:
                    new_step[x+dx, y+dy] += 1


def play_step(step):
    # increase energy
    new_step = {k: v+1 for k, v in step.items()}
    flashed = True
    flashes = 0
    while flashed:
        flashed = False
        for (x, y), octopus in new_step.items():
            if octopus > 9:
                flash(new_step, x, y)
                flashes += 1
                flashed = True
    return new_step, flashes


def part_1(print_result: bool = True) -> int:
    octopuses = parse_data()
    flashes = 0
    for _ in range(100):
        octopuses, step_flashes = play_step(octopuses)
        flashes += step_flashes
    if print_result:
        print_map((0, 9, 0, 9), lambda x, y: str(octopuses[(x, y)]))
    return flashes


def part_2(print_result: bool = True) -> int:
    octopuses = parse_data()
    step = 0
    while True:
        step += 1
        octopuses, step_flashes = play_step(octopuses)
        if step_flashes == 100:
            break
    if print_result:
        print_map((0, 9, 0, 9), lambda x, y: str(octopuses[(x, y)]))
    return step


SOLUTION_1 = 1673
SOLUTION_2 = 279

if __name__ == "__main__":
    print(part_1())
    print(part_2())
