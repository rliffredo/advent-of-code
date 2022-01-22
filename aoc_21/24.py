import re

from common import read_data


def parse_data(compiled):
    lines = read_data("24", False)
    return convert_to_python(lines, compiled)


def convert_to_python(alu_instructions, compiled):
    instructions = alu_instructions
    # special cases
    instructions = re.sub(r"div . 1\n", r"", instructions)
    instructions = re.sub(r"eql x w\neql x 0", r"x = 1 if x != w else 0", instructions)
    for r in "xywz":
        instructions = re.sub(f"mul {r} 0\nadd {r} (.*)", f"{r} = \\1", instructions)
    # basic instruction
    instructions = re.sub(r"add (.) (.*)", r"\1 = \1 + \2", instructions)
    instructions = re.sub(r"mul (.) (.*)", r"\1 = \1 * \2", instructions)
    instructions = re.sub(r"div (.) (.*)", r"\1 = \1 // \2", instructions)
    instructions = re.sub(r"mod (.) (.*)", r"\1 = \1 % \2", instructions)
    instructions = re.sub(r"eql (.) (.*)", r"\1 = 1 if (\1 == \2) else 0", instructions)
    # input
    for n in range(14):
        instructions = re.sub(r"inp w", f"\nif r=={n}: ret = z\n\nw = n[{n}]", instructions, count=1)

    # special postprocessing
    instructions = re.sub(r"x = x \+ (.+)\nx = 1 if x != w", r"k1 = \1\nx = x + k1\nx = 1 if x != w", instructions)
    instructions = re.sub(r"y = w\ny = y \+ (.*)", r"k2 = \1\ny = w + k2", instructions)
    instructions = re.sub(r"z = z // 26", r"k3 = True\nif k3:\n    z = z // 26", instructions)
    instructions = re.sub(r"x = x % 26\nk1", r"x %= 26\nk3 = False\nif k3:\n    z //= 26\nk1", instructions)
    code_str = "x, y, z = 0, 0, 0\n" + instructions + "\nif r==14: ret = z\n"

    return compile(code_str, filename="<string>", mode="exec") if compiled else code_str


def calc_z_for_number(instructions, number) -> int:
    exec_vars = {"n": [int(n) for n in number], "r": len(number)}
    exec(instructions, exec_vars)
    return exec_vars["ret"]


def calc_z_for_digit(w, z, level):
    k1, k2, k3 = calc_z_for_digit.params[level]
    x = z
    if k3:
        z = z // 26
    if w == (x % 26) + k1:
        return z
    else:
        return z * 26 + w + k2


calc_z_for_digit.params = [
    (11, 14, False),
    (13, 8, False),
    (11, 4, False),
    (10, 10, False),
    (-3, 14, True),
    (-4, 10, True),
    (12, 4, False),
    (-8, 14, True),
    (-3, 1, True),
    (-12, 6, True),
    (14, 0, False),
    (-6, 9, True),
    (11, 13, False),
    (-12, 12, True),
]


def get_best_valid_number(search_range):
    def find_number_with_zero_z(z_input, digit_pos_in_number, digits_so_far):

        if digit_pos_in_number == 14:
            if z_input == 0:
                return digits_so_far
            return None

        # First optimization: recognize if the results are all the same on this level
        z_to_n = {calc_z_for_digit(n, z_input, digit_pos_in_number): n for n in search_range}

        # Second optimization: recognize if digit_z(x) is the same for any two numbers. If so, remove the lower
        if digit_pos_in_number < 13:
            found_values = set()
            nested = digit_pos_in_number + 1
            unique_digits = []
            all_values = []
            for z_output, digit in z_to_n.items():
                nested_values = tuple((sub_digit, calc_z_for_digit(sub_digit, z_output, nested))
                                      for sub_digit in search_range)
                if nested_values not in found_values:
                    found_values.add(nested_values)
                    unique_digits.append((z_output, digit))
                all_values.append(nested_values)
        else:
            unique_digits = z_to_n.items()

        for z_output, digit in unique_digits:
            number_to_evaluate = digits_so_far + [digit]
            result = find_number_with_zero_z(z_output, digit_pos_in_number + 1, number_to_evaluate)
            if result:
                return result

        return None

    res = find_number_with_zero_z(0, 0, [])
    return int("".join(str(d) for d in res)) if res else -1


def calc_z_for_number_no_data(n):
    z = 0
    for p, d in enumerate(n):
        z_in = z
        z = calc_z_for_digit(int(d), z, p)
        print(int(d), z_in, z)
    return z


def part_1(print_result: bool = True) -> int:
    if print_result:
        print(f"74929995999389 has z: {calc_z_for_number(parse_data(True), '74929995999389')}")
        print(f"74929995999389 has z: {calc_z_for_number_no_data('74929995999389')}")
        print("Code converted:")
        print(parse_data(False))

    return get_best_valid_number(list(range(9, 0, -1)))


def part_2(print_result: bool = True) -> int:
    return get_best_valid_number(list(range(1, 10)))


SOLUTION_1 = 74929995999389
SOLUTION_2 = 11118151637112

IS_SOLUTION_1_SLOW = True
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
