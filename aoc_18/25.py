from collections import namedtuple
from typing import List, Dict, Tuple, Set

Star = namedtuple('Star', 'x,y,z,t')


def parse_line(line: str) -> Star:
    return Star(*[int(n) for n in line.split(',')])


def parse_file(subdir='.') -> List[Star]:
    data = open(f'{subdir}/input_25.txt').readlines()
    parsed = [parse_line(d) for d in data]
    return parsed


def distance(p1: Star, p2: Star) -> int:
    return sum(abs(p1[i] - p2[i]) for i in (0, 1, 2, 3))


def all_distances(stars: List[Star]):
    distances = {}
    n_stars = len(stars)
    for i in range(n_stars):
        for j in range(i + 1, n_stars):
            distances[(stars[i], stars[j])] = distance(stars[i], stars[j])
    return distances


def find_constellations(stars: List[Star]) -> Dict[Star, Set[Star]]:
    constellations: Dict[Star, Set[Star]] = {}
    to_analyze = set(stars)
    while to_analyze:
        current_star = to_analyze.pop()
        print(f'*** Analyzing {current_star} ({len(to_analyze)} left) ***')
        if add_star_to_constellations(current_star, constellations):
            continue
        constellations[current_star] = {current_star}
        added_stars = set()
        for star in to_analyze:
            added = add_star_to_constellations(star, constellations)
            if added:
                added_stars.add(star)
        to_analyze.difference_update(added_stars)

    return constellations


def add_star_to_constellations(star: Star, constellations: Dict[Star, Set[Star]]) -> bool:
    added = False
    star_constellations: List[Star] = []
    for constellation_key in constellations:
        for constellation_star in constellations[constellation_key]:
            dist = distance(constellation_star, star)
            if dist <= 3:
                constellations[constellation_key].add(star)
                star_constellations.append(constellation_key)
                added = True
                break
    for i in range(1, len(star_constellations)):
        constellation_key_base = star_constellations[0]
        constellation_key_to_merge = star_constellations[i]
        constellations[constellation_key_base].update(constellations[constellation_key_to_merge])
        del (constellations[constellation_key_to_merge])
    return added


def count_constellations():
    stars = parse_file()
    all_constellations = find_constellations(stars)
    print(f'######\nThere are {len(all_constellations)} constellations')
    for constellation in all_constellations.values():
        print(f' - {constellation}')


count_constellations()
