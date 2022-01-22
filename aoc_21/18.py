import functools
import itertools
import math
from typing import Tuple, Union, Optional

from common import read_data


def parse_snail_number(raw_number):
    def _parse_number(number_str: str):
        current_char = 0
        assert number_str[current_char] == "["
        current_char += 1
        if number_str[current_char] == "[":
            left, delta_char = _parse_number(number_str[current_char:])
            current_char += delta_char
        else:
            left = int(number_str[current_char], base=16)
            current_char += 1
        assert number_str[current_char] == ","
        current_char += 1
        if number_str[current_char] == "[":
            right, delta_char = _parse_number(number_str[current_char:])
            current_char += delta_char
        else:
            right = int(number_str[current_char], base=16)
            current_char += 1
        return (left, right), current_char + 1

    return _parse_number(raw_number)[0]


def parse_data():
    raw_numbers = read_data("18", True)
    numbers = [parse_snail_number(raw_number) for raw_number in raw_numbers]
    return numbers


def snail_explode(number_to_explode):
    def add_to_pair_right(pair, number):
        assert isinstance(number, int)
        if isinstance(pair, int):
            return pair + number
        left, right = pair
        return left, add_to_pair_right(right, number)

    def add_to_pair_left(pair, number):
        assert isinstance(number, int)
        if isinstance(pair, int):
            return pair + number
        left, right = pair
        return add_to_pair_left(left, number), right

    def explode_pair(number, depth) -> Tuple[Union[int, Tuple], Optional[int], Optional[int], bool]:
        """
        Returns the pair (or what should be in its stead), and then if necessary, numbers to be added left and right
        """
        if isinstance(number, int):
            # It's a number, so no need to do anything
            return number, None, None, False

        left, right = number
        if depth == 4:
            # We need to explode. Also, we know that left and right are numbers
            assert isinstance(left, int)
            assert isinstance(right, int)
            return 0, left, right, True

        # Depth is less than 4, so we need to go on the "numbers" inside
        # - Explode left first
        left_value, left_sum_left, left_sum_right, left_pair_exploded = explode_pair(left, depth + 1)
        assert isinstance(left_sum_left, int) or left_sum_left is None
        assert isinstance(left_sum_right, int) or left_sum_right is None
        if left_sum_left or left_sum_right:
            # exploded left pair. We need to propagate the changes
            if left_sum_right is not None:
                right_value = add_to_pair_left(right, left_sum_right)
            else:
                right_value = right
            return (left_value, right_value), left_sum_left, None, True

        if left_pair_exploded:
            return (left_value, right), 0, 0, True

        # No pair on the left exploded, so let's go on right
        right_value, right_sum_left, right_sum_right, right_pair_exploded = explode_pair(right, depth + 1)
        assert isinstance(right_sum_left, int) or right_sum_left is None
        assert isinstance(right_sum_right, int) or right_sum_right is None
        if right_sum_left or right_sum_right:
            # exploded right pair. We need to propagate the changes
            if right_sum_left is not None:
                left_value = add_to_pair_right(left, right_sum_left)
            else:
                left_value = left
            return (left_value, right_value), None, right_sum_right, True

        # No pair on left or right exploded, so let's go up quietly
        new_number = left_value, right_value
        return new_number, 0, 0, right_pair_exploded

    exploded_number = explode_pair(number_to_explode, 0)[0]
    has_exploded = exploded_number != number_to_explode
    return exploded_number, has_exploded


def snail_split(snail_number):
    if isinstance(snail_number, int):
        if snail_number < 10:
            return snail_number, False
        left = int(math.floor(snail_number / 2))
        right = int(math.ceil(snail_number / 2))
        return (left, right), True

    left, right = snail_number
    split_left, has_split = snail_split(left)
    if has_split:
        return (split_left, right), True
    split_right, has_split = snail_split(right)
    if has_split:
        return (left, split_right), True
    return snail_number, False


def snail_reduce(number):
    while True:
        number, was_exploded = snail_explode(number)
        if was_exploded:
            continue
        number, was_split = snail_split(number)
        if not was_split:
            break
    return number


def snail_addition(a, b):
    return a, b


def snail_sum(a, b):
    new_number = snail_addition(a, b)
    return snail_reduce(new_number)


def snail_magnitude(snail_number):
    if isinstance(snail_number, int):
        return snail_number
    left, right = snail_number
    return snail_magnitude(left) * 3 + snail_magnitude(right) * 2


def test_parse():
    print("\nTEST PARSE")
    test_data = [
        "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
        "[[[[0,7],4],[7,[[8,4],9]]],[1,1]]",
        "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]",
        "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
    ]
    for d in test_data:
        try:
            print(f"PASSED: {d} -> {parse_snail_number(d)}")
        except AssertionError as error:
            print(f"FAILED: {d} -> {error}")


def test_explode():
    print("\nTEST EXPLODE")
    test_data = [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
        ("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"),
        ("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"),
        ("[[[[[4,9],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,D],4],[7,[[8,4],9]]],[1,1]]"),
        ("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[F,[0,D]]],[1,1]]"),
        ("[[[[0,[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]",
         "[[[[5,0],[[B,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]]"),
    ]

    for d in test_data:
        if snail_explode(parse_snail_number(d[0]))[0] == parse_snail_number(d[1]):
            print(f"PASSED: {d[0]} -> {d[1]}")
        else:
            print(f"FAILED: {d[0]} -> {snail_explode(parse_snail_number(d[0]))[0]} "
                  f"/ expected: {parse_snail_number(d[1])}")


def test_sum():
    print("\nTEST SUM")
    test_data = [
        ("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", "[5,5]", "[[[[3,0],[5,3]],[4,4]],[5,5]]"),
        ("[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]", "[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
         "[[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]]"),
    ]

    for d in test_data:
        sn1 = parse_snail_number(d[0])
        sn2 = parse_snail_number(d[1])
        expected_sum = parse_snail_number(d[2])
        sn_sum = snail_sum(sn1, sn2)
        if sn_sum == expected_sum:
            print(f"PASSED: {d[0] + d[1]} -> {d[2]}")
        else:
            print(f"FAILED: {d[0]} + {d[1]} -> {sn_sum}  / expected: {expected_sum}")


def test_magnitude():
    print("\nTEST MAGNITUDE")
    test_data = [
        ("[[1,2],[[3,4],5]]", 143),
        ("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", 1384),
        ("[[[[1,1],[2,2]],[3,3]],[4,4]]", 445),
        ("[[[[3,0],[5,3]],[4,4]],[5,5]]", 791),
        ("[[[[5,0],[7,4]],[5,5]],[6,6]]", 1137),
        ("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]", 3488),
    ]

    for d in test_data:
        if snail_magnitude(parse_snail_number(d[0])) == d[1]:
            print(f"PASSED: {d[0]} -> {d[1]}")
        else:
            print(f"FAILED: {d[0]} -> {snail_magnitude(parse_snail_number(d[0]))}  / expected: {d[1]}")


def part_1(print_result: bool = True) -> int:
    if print_result:
        test_parse()
        test_explode()
        test_sum()
        test_magnitude()
        print("\n")
    snail_numbers = parse_data()
    summed = functools.reduce(lambda x, y: snail_sum(x, y), snail_numbers)
    return snail_magnitude(summed)


def part_2(print_result: bool = True) -> int:
    snail_numbers = parse_data()
    all_couples = itertools.permutations(snail_numbers, 2)
    all_sums = (snail_sum(a, b) for a, b in all_couples)
    all_magnitudes = (snail_magnitude(s) for s in all_sums)
    return max(all_magnitudes)


SOLUTION_1 = 4641
SOLUTION_2 = 4624

IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
