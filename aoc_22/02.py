from common import read_data


def _to_int(r):
    return {
        'A': 0, 'B': 1, 'C': 2,
        'X': 0, 'Y': 1, 'Z': 2,
    }[r]


def parse_data():
    lines = read_data('02', True)
    rounds = [l.split() for l in lines if l]
    regular_rounds = [(_to_int(r[0]), _to_int(r[1])) for r in rounds]
    return regular_rounds


def _match_score(me, opponent) -> int:
    # The truth table for the result can be shortened
    # using modulo.
    return ((me - opponent + 1) % 3) * 3


def calc_round_score(opponent, me):
    match_score = _match_score(me, opponent)
    score = me + 1 + match_score
    return score


def part_1() -> int:
    rounds = parse_data()
    scores = [calc_round_score(r[0], r[1]) for r in rounds]
    return sum(scores)


def _match_choice(opponent: int, result: int) -> int:
    # The truth table for the result can be shortened
    # using modulo.
    return (opponent + result - 1) % 3


def calc_round_2(r):
    my_choice = _match_choice(r[0], r[1])
    return calc_round_score(r[0], my_choice)


def part_2() -> int:
    rounds = parse_data()
    scores = [calc_round_2(r) for r in rounds]
    return sum(scores)


SOLUTION_1 = 11475
SOLUTION_2 = 16862

if __name__ == '__main__':
    print(part_1())
    print(part_2())
