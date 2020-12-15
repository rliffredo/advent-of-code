INPUT = [9, 3, 1, 0, 8, 4]


def get_spoken_after(max_turns, verbose):
    # starting numbers
    turn_numbers = {n: (0, turn + 1) for turn, n in enumerate(INPUT)}
    current_turn = len(turn_numbers)
    last_spoken = INPUT[-1]
    # start_playing
    while current_turn < max_turns:
        current_turn += 1
        if last_spoken not in turn_numbers:
            last_spoken = 0
        else:
            last_spoken_information = turn_numbers[last_spoken]
            if last_spoken_information[0] == 0:
                last_spoken = 0
            elif last_spoken in turn_numbers:
                last_spoken = last_spoken_information[1] - last_spoken_information[0]
        if last_spoken not in turn_numbers:
            turn_numbers[last_spoken] = current_turn, current_turn
        else:
            turn_numbers[last_spoken] = turn_numbers[last_spoken][1], current_turn
        if verbose and current_turn % 1000000 == 0:
            print(".", end="")
    return last_spoken


def part_1(print_result: bool = True) -> int:
    last_spoken = get_spoken_after(2020, print_result)

    if print_result:
        print(f"Result is {last_spoken}")
    return last_spoken


def part_2(print_result: bool = True) -> int:
    if print_result:
        print("Calculating (will take a while) ", end="")

    last_spoken = get_spoken_after(30_000_000, print_result)

    if print_result:
        print(f"Result is {last_spoken}")
    return last_spoken


SOLUTION_1 = 371
SOLUTION_2 = 352
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    part_1()
    part_2()
