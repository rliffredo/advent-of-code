INPUT = [9, 3, 1, 0, 8, 4]


def get_spoken_after(max_turns):
    # starting numbers
    turn_numbers = {n: turn + 1 for turn, n in enumerate(INPUT)}
    spoken = 0
    # start_playing
    for current_turn in range(len(turn_numbers)+1, max_turns):
        if spoken not in turn_numbers:
            last_time = current_turn
            turn_numbers[spoken] = current_turn
        else:
            last_time = turn_numbers[spoken]
            turn_numbers[spoken] = current_turn
        spoken = current_turn - last_time

    return spoken


def part_1(print_result: bool = True) -> int:
    last_spoken = get_spoken_after(2020)

    if print_result:
        print(f"After 2020 turns, last spoken is {last_spoken}")
    return last_spoken


def part_2(print_result: bool = True) -> int:
    if print_result:
        print("Calculating last spoken after 30M turns (will take a while)... ", end="")

    last_spoken = get_spoken_after(30_000_000)

    if print_result:
        print(f"{last_spoken}")
    return last_spoken


SOLUTION_1 = 371
SOLUTION_2 = 352
IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    part_1()
    part_2()
