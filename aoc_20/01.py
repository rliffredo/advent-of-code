from common import read_data

raw_numbers = read_data("01", True)
all_numbers = {int(n) for n in raw_numbers}


def find_pairs_for_sum(numbers, k):
    for number in numbers:
        other_number = k - number
        if other_number in numbers:
            return True, number, other_number
    else:
        return False, 0, 0


res = find_pairs_for_sum(all_numbers, 2020)
if res[0]:
    print(f"Found {res[1]} and {res[2]}, their product is {res[1]*res[2]}")
else:
    print("No pair found!")


def find_thrice_for_sum(numbers, k):
    numbers_to_check = {n for n in numbers}
    while numbers_to_check:
        n0 = numbers_to_check.pop()
        partial_sum = k-n0
        res, n1, n2 = find_pairs_for_sum(numbers_to_check, partial_sum)
        if res:
            return res, n0, n1, n2
    return False, 0, 0, 0


res = find_thrice_for_sum(all_numbers, 2020)
if res[0]:
    print(f"Found {res[1]}, {res[2]}, {res[3]}, their product is {res[1]*res[2]*res[3]}")
else:
    print("No thrice found!")
