from common import read_data


def parse_data():
    raw_numbers = read_data("01", True)
    return {int(n) for n in raw_numbers}


def find_pairs_for_sum(numbers, k):
    for number in numbers:
        other_number = k - number
        if other_number in numbers:
            return True, number, other_number
    else:
        return False, 0, 0


def part_1(print_result: bool = True) -> int:
    all_numbers = parse_data()
    res = find_pairs_for_sum(all_numbers, 2020)
    assert res[0], "A pair must exists"
    pair_product = res[1] * res[2]
    if print_result:
        print(f"Found {res[1]} and {res[2]}, their product is {pair_product}")
    return pair_product


def find_thrice_for_sum(numbers, k):
    numbers_to_check = {n for n in numbers}
    while numbers_to_check:
        n0 = numbers_to_check.pop()
        partial_sum = k-n0
        res, n1, n2 = find_pairs_for_sum(numbers_to_check, partial_sum)
        if res:
            return res, n0, n1, n2
    return False, 0, 0, 0


def part_2(print_result: bool = True) -> int:
    all_numbers = parse_data()
    res = find_thrice_for_sum(all_numbers, 2020)
    assert res[0], "A thrice must exists"
    thrice_product = res[1]*res[2]*res[3]
    if print_result:
        print(f"Found {res[1]}, {res[2]}, {res[3]}, their product is {thrice_product}")
    return thrice_product


SOLUTION_1 = 806656
SOLUTION_2 = 230608320

if __name__ == "__main__":
    part_1()
    part_2()

