from common import read_data


def get_position_first_unique_buffer(chars, buffer_len):
    """
    We can determine the buffer by transforming to a set
    and checking the length, because a set will remove
    duplicated elements.
    """
    return next(pos
                for pos in range(buffer_len, len(chars))
                if len(set(chars[pos - buffer_len:pos])) == buffer_len)


def part_1(print_result: bool = True) -> int:
    chars = read_data("06")
    return get_position_first_unique_buffer(chars, 4)


def part_2(print_result: bool = True) -> int:
    chars = read_data("06")
    return get_position_first_unique_buffer(chars, 14)


SOLUTION_1 = 1080
SOLUTION_2 = 3645

if __name__ == "__main__":
    print(part_1())
    print(part_2())
