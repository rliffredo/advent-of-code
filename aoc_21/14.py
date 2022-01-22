from collections import Counter

from common import read_data, pairwise


def parse_data():
    raw_data = read_data("14", True)
    start = ["".join(p) for p in pairwise(raw_data[0])]
    plain_subs = [l.split(" -> ") for l in raw_data[2:]]
    subs = {
        k: (k[0] + v, v + k[1])
        for k, v in plain_subs
    }
    return start, subs


def polimerize_elements(start, subs, times):
    poly = Counter(start)
    for n in range(times):
        new_poly = Counter()
        for p in poly:
            p1, p2 = subs[p]
            new_poly[p1] += poly[p]
            new_poly[p2] += poly[p]
        poly = new_poly
    c = Counter()
    for p in poly:
        c[p[0]] += poly[p]
    c[start[-1][-1]] += 1
    return c


def polimerization_factor(elements_counter):
    return elements_counter.most_common()[0][1] - elements_counter.most_common()[-1][1]


def part_1(print_result: bool = True) -> int:
    start, subs = parse_data()
    element_counts = polimerize_elements(start, subs, 10)
    return polimerization_factor(element_counts)


def part_2(print_result: bool = True) -> int:
    start, subs = parse_data()
    element_counts = polimerize_elements(start, subs, 40)
    return polimerization_factor(element_counts)


SOLUTION_1 = 3306
SOLUTION_2 = 3760312702877

if __name__ == "__main__":
    print(part_1())
    print(part_2())
