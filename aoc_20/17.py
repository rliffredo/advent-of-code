from collections import defaultdict

from common import read_data


def parse_data(dimensions):
    raw_data = read_data("17", True)
    return {(x, y) + (0,) * (dimensions - 2)
            for y, line in enumerate(raw_data)
            for x, state in enumerate(line)
            if state == "#"}


def neighbours_3d(cube):
    return [(x, y, z)
            for x in range(cube[0] - 1, cube[0] + 2)
            for y in range(cube[1] - 1, cube[1] + 2)
            for z in range(cube[2] - 1, cube[2] + 2)]


def neighbours_4d(cube):
    neighbours = [(x, y, z, w)
                  for x in [cube[0] - 1, cube[0], cube[0] + 1]
                  for y in [cube[1] - 1, cube[1], cube[1] + 1]
                  for z in [cube[2] - 1, cube[2], cube[2] + 1]
                  for w in [cube[3] - 1, cube[3], cube[3] + 1]]
    return neighbours


def will_be_active(cube, neighbours, matrix):
    # Count neighbours.
    # This is the most performance-critical part, so we are going to use a
    # couple of small optimizations: use an explicit loop instead of a
    # generator, and exit earlier as soon as we know that there are more than
    # three neighbours
    active_neighbours = 0
    for neighbour in neighbours:
        if neighbour in matrix and neighbour != cube:
            active_neighbours += 1
        if active_neighbours > 3:
            return False
    # Life rules
    if active_neighbours == 3:
        return True
    return cube in matrix and active_neighbours == 2


def play_game_of_life(turns, dimensions, get_neighbours):
    matrix = parse_data(dimensions=dimensions)
    for _ in range(turns):
        cube_neighbours = defaultdict(set)
        for cube in matrix:
            for ne in get_neighbours(cube):
                cube_neighbours[ne].add(cube)
        matrix = {cube
                  for cube, neighbours in cube_neighbours.items()
                  if will_be_active(cube, neighbours, matrix)}
    active_cubes = len(matrix)
    return active_cubes


def part_1(print_result: bool = True) -> int:
    active_cubes = play_game_of_life(6, 3, neighbours_3d)
    if print_result:
        print(f"After six iterations in 3D there are {active_cubes} active cubes")
    return active_cubes


def part_2(print_result: bool = True) -> int:
    active_cubes = play_game_of_life(6, 4, neighbours_4d)
    if print_result:
        print(f"After six iterations in 4D there are {active_cubes} active cubes")
    return active_cubes


SOLUTION_1 = 319
SOLUTION_2 = 2324

if __name__ == "__main__":
    part_1()
    part_2()
