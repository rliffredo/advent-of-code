def part_1(print_result: bool = True) -> int:
    pk_card, pk_door = 1614360, 7734663
    size = 20201227

    looked_pks = pk_card, pk_door
    for loop_size in range(size):
        estimated_pk = pow(7, loop_size, size)
        if estimated_pk not in looked_pks:
            continue
        if estimated_pk == pk_card:
            encryption_key = pow(pk_door, loop_size, size)
            break
        elif estimated_pk == pk_door:
            encryption_key = pow(pk_card, loop_size, size)
            break
    else:
        assert False, "There is a solution!"

    if print_result:
        print(f"Encryption key is {encryption_key}")
    return encryption_key


def part_2(print_result: bool = True) -> int:
    if print_result:
        print("All done!")
    return 50


SOLUTION_1 = 5414549
SOLUTION_2 = 50
IS_SOLUTION_1_SLOW = True


if __name__ == "__main__":
    part_1()
    part_2()
