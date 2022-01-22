from common import read_data


def parse_data():
    def parse_command(cr):
        cmd, amt = cr.split(" ")
        return cmd, int(amt)

    command_raws = read_data("02", True)
    command_pairs = [parse_command(cr) for cr in command_raws]
    return command_pairs


def exec_command_1(cmd, amt, position):
    if cmd == "forward":
        return position[0] + amt, position[1]
    elif cmd == "down":
        return position[0], position[1] + amt
    elif cmd == "up":
        return position[0], position[1] - amt
    else:
        assert False, cmd


def part_1(print_result: bool = True) -> int:
    commands = parse_data()
    position = 0, 0
    for cmd in commands:
        position = exec_command_1(*cmd, position)
    return position[0] * position[1]


def exec_command_2(cmd, amt, position):
    if cmd == "forward":
        return position[0] + amt, position[1] + position[2] * amt, position[2]
    elif cmd == "down":
        return position[0], position[1], position[2] + amt
    elif cmd == "up":
        return position[0], position[1], position[2] - amt
    else:
        assert False, cmd


def part_2(print_result: bool = True) -> int:
    commands = parse_data()
    position = 0, 0, 0
    for cmd in commands:
        position = exec_command_2(*cmd, position)
    return position[0] * position[1]


SOLUTION_1 = 2120749
SOLUTION_2 = 2138382217

if __name__ == "__main__":
    print(part_1())
    print(part_2())
