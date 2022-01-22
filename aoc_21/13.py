from advent_of_code_ocr import convert_6

from common import read_data, make_map


def parse_data():
    raw_data = read_data("13", True)
    points = set()
    folding_instructions = []
    is_point = True
    for line in raw_data:
        is_point = is_point and bool(line)
        if not line:
            continue
        if is_point:
            point_coords = tuple(int(n) for n in line.split(","))
            points.add(point_coords)
        else:
            instruction = line.split()[2].split("=")
            folding_instructions.append((instruction[0], int(instruction[1])))
    return points, folding_instructions


def fold_point(x, y, axis, value):
    if axis == "x":
        return value - abs(x - value), y
    else:
        return x, value - abs(y - value)


def fold(points, axis, value):
    return {fold_point(x, y, axis, value) for x, y in points}


def part_1(print_result: bool = True) -> int:
    points, folding_instructions = parse_data()
    folded_map = fold(points, *folding_instructions[0])
    return len(folded_map)


def part_2(print_result: bool = True) -> str:
    points, folding_instructions = parse_data()
    for instruction in folding_instructions:
        points = fold(points, *instruction)
    result = make_map((0, max(p[0] for p in points), 0, max(p[1] for p in points)),
                      lambda x, y: "#" if (x, y) in points else ".")
    if print_result:
        print(result)

    return convert_6(result)


SOLUTION_1 = 814
SOLUTION_2 = "PZEHRAER"

if __name__ == "__main__":
    print(part_1())
    print(part_2())
