from common import read_data


def parse_data():
    return read_data("03", True)


def analyze_column(column, diagnostic_lines, find_most_common):
    """
    Analyze columns to find the most/least common value.
    We explot the fact that they are just 0 or 1, so we can simply sum all
    values, and then see if it's more (or less) than 50%.
    """
    pred = (lambda x, y: x >= y) if find_most_common else (lambda x, y: x < y)
    total_lines = len(diagnostic_lines)
    total_bits = sum(int(diag[column]) for diag in diagnostic_lines)
    most_common = str(int(pred(total_bits, total_lines / 2)))
    return most_common


def calc_rate(diagnostic_lines, is_gamma):
    line_length = len(diagnostic_lines[0])
    bits = [analyze_column(i, diagnostic_lines, is_gamma) for i in range(line_length)]
    bits_str = "".join(bits)
    return int(bits_str, 2)


def part_1(print_result: bool = True) -> int:
    diagnostic_lines = parse_data()
    gamma = calc_rate(diagnostic_lines, True)
    epsilon = calc_rate(diagnostic_lines, False)
    return gamma * epsilon


def calc_filter_rating(diagnostic_lines, is_oxygen):
    line_length = len(diagnostic_lines[0])
    for current_column in range(line_length):
        most_common = analyze_column(current_column, diagnostic_lines, is_oxygen)
        diagnostic_lines = [
            line for line in diagnostic_lines
            if line[current_column] == most_common
        ]
        if len(diagnostic_lines) == 1:
            break
    else:
        assert False, "Ops!"
    return int(diagnostic_lines[0], 2)


def part_2(print_result: bool = True) -> int:
    diagnostic_lines = parse_data()
    oxygen_generator_rating = calc_filter_rating(diagnostic_lines, True)
    co2_scrubbing_rating = calc_filter_rating(diagnostic_lines, False)
    return oxygen_generator_rating * co2_scrubbing_rating


SOLUTION_1 = 4138664
SOLUTION_2 = 4273224

if __name__ == "__main__":
    print(part_1())
    print(part_2())
