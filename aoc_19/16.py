import itertools
from time import process_time

from common import read_data, take


def parse_to_list(input_string):
    return [int(n) for n in input_string]


################
# ## PART 1 ## #
################

def pattern_for_element(element_pos, total_elems):
    base_pattern = [0, 1, 0, -1]
    position_one_base = element_pos + 1
    actual_pattern = itertools.chain.from_iterable([p] * position_one_base for p in base_pattern)
    repeated_pattern = itertools.cycle(actual_pattern)
    next(repeated_pattern)
    index_all = [n for n in take(total_elems, repeated_pattern)]
    return [i for i in range(total_elems) if index_all[i] == 1], [i for i in range(total_elems) if index_all[i] == -1]


def get_digit_value(input_list, digit_pos, patterns):
    value = sum(input_list[i] for i in patterns[digit_pos][0]) - sum(input_list[i] for i in patterns[digit_pos][1])
    n = abs(value)
    while n >= 10:
        n = n % 10
    return n


def calc_phase(input_list):
    start = process_time()
    input_len = len(input_list)
    patterns = [pattern_for_element(i, input_len) for i in range(input_len)]
    for _ in range(100):
        input_list = [get_digit_value(input_list, n, patterns) for n in range(input_len)]
    end = process_time()

    print(f'Time required: {end - start}')  # 1.25s
    return ''.join(map(str, input_list[:8]))


print(f'After 100 iterations, result is {calc_phase(parse_to_list(read_data("16")))}')  # 36627552


################
# ## PART 2 ## #
################

def calc_phase_offset(input_digits, offset):
    """
    The complexity of the calculation is O(n2); however, we can simplify if greatly, by analyzing the input data:
    - All coefficient left of the number are zero
         -> skip calculation of all digits before the offset
    - The offset is far enough, that all coefficient at that point are 1
         -> each number is just the sum of all the following
    """
    all_digits = input_digits*10000
    useful_digits = all_digits[offset:]

    start = process_time()
    for _ in range(100):
        for i in range(len(useful_digits)-2, -1, -1):  # iterate backward on the list
            useful_digits[i] = (useful_digits[i] + useful_digits[i+1]) % 10
    end = process_time()
    print(f'Time required: {end - start}')  # 8s

    return ''.join(map(str, useful_digits[:8]))


string_digits = read_data("16")
input_digits = parse_to_list(string_digits)
offset = int(string_digits[:7])
print(f'After 100 iterations, result at offset {offset} is {calc_phase_offset(input_digits, offset)}')  # 79723033
