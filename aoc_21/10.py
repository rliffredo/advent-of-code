from common import read_data


def parse_data():
    return read_data("10", True)


def get_wrong_chars(line):
    stack = []
    for char in line:
        if char in "([{<":
            stack.append(char)
        else:
            opening_char = stack.pop()
            matching_char = {"(": ")", "[": "]", "{": "}", "<": ">"}[opening_char]
            if char != matching_char:
                return char, ""
    remaining_chars = [{"(": ")", "[": "]", "{": "}", "<": ">"}[c] for c in stack[::-1]]
    return "", "".join(remaining_chars)


def calc_line_point(line):
    return {")": 3, "]": 57, "}": 1197, ">": 25137}.get(get_wrong_chars(line)[0], 0)


def part_1(print_result: bool = True) -> int:
    return sum(calc_line_point(line) for line in parse_data())


def calc_legal_line_point(line):
    score = 0
    for mc in get_wrong_chars(line)[1]:
        score *= 5
        score += {")": 1, "]": 2, "}": 3, ">": 4}.get(mc, 0)
    return score


def part_2(print_result: bool = True) -> int:
    scores = [calc_legal_line_point(line) for line in parse_data()]
    legal_scores = sorted(s for s in scores if s)
    return legal_scores[len(legal_scores) // 2]


SOLUTION_1 = 311895
SOLUTION_2 = 2904180541

if __name__ == "__main__":
    print(part_1())
    print(part_2())
