from common import read_data, print_map


def parse_data():
    lines = read_data("20", True)
    raw_mask = lines[0]
    mask = [str(int(c == "#")) for c in raw_mask]
    image_raw = lines[2:]
    image = {
        (x, y): str(int(char == "#"))
        for y, image_line in enumerate(image_raw)
        for x, char in enumerate(image_line)
    }
    return mask, image


def print_trench_map(trench_map):
    sizes = get_image_sizes(trench_map)
    margin = 1
    sizes = (sizes[0] - margin, sizes[1] + margin, sizes[2] - margin, sizes[3] + margin)
    print_map(sizes, lambda x, y: "#" if trench_map.get((x, y), "0") == "1" else ".")


def get_image_sizes(trench_map):
    min_x = min(k[0] for k in trench_map)
    max_x = max(k[0] for k in trench_map)
    min_y = min(k[1] for k in trench_map)
    max_y = max(k[1] for k in trench_map)
    return min_x, max_x, min_y, max_y


def enhance_pixel(pixel, trench_map, image_mask, default):
    mask_index_binary = "".join([
        trench_map.get((x, y), default)
        for y in [pixel[1] - 1, pixel[1], pixel[1] + 1]
        for x in [pixel[0] - 1, pixel[0], pixel[0] + 1]
    ])
    mask_index = int(mask_index_binary, base=2)
    return image_mask[mask_index]


def enhance_image(trench_map, image_mask, default):
    offset = 1
    sizes = get_image_sizes(trench_map)
    min_x, max_x, min_y, max_y = sizes
    new_trench_map = {
        (x, y): enhance_pixel((x, y), trench_map, image_mask, default)
        for x in range(min_x - offset, max_x + 1 + offset)
        for y in range(min_y - offset, max_y + 1 + offset)
    }
    return new_trench_map


def enhance_trench_map(iterations, trench_map, image_mask, print_result):
    default = "0"
    for n in range(iterations):
        trench_map = enhance_image(trench_map, image_mask, default)
        default = enhance_pixel((1, 1), {}, image_mask, default)
        if print_result:
            print(f"\nITERATION {n}")
            print_trench_map(trench_map)
    return trench_map


def part_1(print_result: bool = True) -> int:
    image_mask, trench_map = parse_data()
    trench_map = enhance_trench_map(2, trench_map, image_mask, print_result)
    lit_pixel = sum(int(n) for n in trench_map.values())
    return lit_pixel


def part_2(print_result: bool = True) -> int:
    image_mask, trench_map = parse_data()
    trench_map = enhance_trench_map(50, trench_map, image_mask, False)
    lit_pixel = sum(int(n) for n in trench_map.values())
    return lit_pixel


SOLUTION_1 = 5819
SOLUTION_2 = 18516

IS_SOLUTION_2_SLOW = True

if __name__ == "__main__":
    print(part_1())
    print(part_2())
