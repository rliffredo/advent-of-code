import re

from common import read_data


def parse_data():
    target_area_def = read_data("17", False)
    matches = re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", target_area_def)
    return tuple(int(n) for n in matches.groups())


def new_probe_position(p):
    px = p[0] + p[2]
    py = p[1] + p[3]
    vx = max(p[2] - 1, 0)
    vy = p[3] - 1
    new_pos = px, py, vx, vy
    return new_pos


def is_in_target(p, tgt):
    return tgt[0] <= p[0] <= tgt[1] and tgt[2] <= p[1] <= tgt[3]


def out_of_target(p, tgt):
    return p[0] > tgt[1] or p[1] < tgt[2]


def fire_probe(vx, vy, tgt):
    max_y = 0
    p = 0, 0, vx, vy
    while not out_of_target(p, tgt):
        max_y = max(max_y, p[1])
        if is_in_target(p, tgt):
            return True, max_y
        p = new_probe_position(p)
    return False, max_y


def get_all_good_trajectories(target):
    if target not in get_all_good_trajectories.cache:
        all_trajectories = [
            (vx, vy, *fire_probe(vx, vy, target))
            for vx in range(1, target[1] + 1)
            # 300 comes "a posteriori", as approximately the minimum still giving the
            # correct result for this exercise. I'm pretty sure we can calculate it
            # in a better way.
            for vy in range(target[2], 300)
        ]
        get_all_good_trajectories.cache[target] = [t for t in all_trajectories if t[2]]
    return get_all_good_trajectories.cache[target]


get_all_good_trajectories.cache = {}


def part_1(print_result: bool = True) -> int:
    target = parse_data()
    results = get_all_good_trajectories(target)
    return max(r[3] for r in results)


def part_2(print_result: bool = True) -> int:
    target = parse_data()
    results = get_all_good_trajectories(target)
    return len(results)


SOLUTION_1 = 35511
SOLUTION_2 = 3282


if __name__ == "__main__":
    print(part_1())
    print(part_2())
