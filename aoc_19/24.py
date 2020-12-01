from common import read_data

SIDE_SIZE = 5
LAYOUT_SIZE = 25


def parse_layout(eris_raw):
    layout = eris_raw.replace('\n', '')
    return layout


################
# ## PART 1 ## #
################

def iterate(layout):
    return ''.join(['#' if is_infested(n, layout) else '.' for n in range(0, LAYOUT_SIZE)])


def is_infested(n, layout):
    neighbours = [n for n in [n - SIDE_SIZE, n + SIDE_SIZE] if 0 <= n < LAYOUT_SIZE]
    x = n % SIDE_SIZE
    if n % SIDE_SIZE > 0:
        neighbours.append(n - 1)
    if n % SIDE_SIZE < SIDE_SIZE - 1:
        neighbours.append(n + 1)
    infested_neighbours = sum(1 for cell in neighbours if layout[cell] == '#')
    infested = (layout[n] == '#' and infested_neighbours == 1) or (layout[n] != '#' and 0 < infested_neighbours <= 2)
    return infested


def calc_biodiversity(layout):
    return sum((1 << pos) * 1 if char == '#' else 0 for pos, char in enumerate(layout))


def get_first_repeated_biodiversity(eris_raw):
    layout = parse_layout(eris_raw)
    biodiversities = {calc_biodiversity(layout)}
    ite = 0
    while True:
        ite = ite + 1
        layout = iterate(layout)
        biodiversity = calc_biodiversity(layout)
        if biodiversity in biodiversities:
            return biodiversity, ite
        biodiversities.add(biodiversity)


bd, it = get_first_repeated_biodiversity(read_data("24"))
print(f'The first repeated biodiversity was {bd}, after {it} iterations')  # 32506764 (63 iterations)

################
# ## PART 2 ## #
################

inner_left = {11}
inner_right = {13}
inner_top = {7}
inner_bottom = {17}
outer_left = set(range(0, LAYOUT_SIZE, SIDE_SIZE))
outer_right = set(range(4, LAYOUT_SIZE, SIDE_SIZE))
outer_top = set(range(0, SIDE_SIZE, 1))
outer_bottom = set(range(20, LAYOUT_SIZE, 1))


def is_cell_on_level_infested(n, level, multi_layout):
    def append_neighbours(neighbour_distance, outer_from, inner_to, inner_from, outer_to):
        if n in outer_from:
            neighbours.extend(multi_layout[level + 1][c] for c in inner_to)
        elif n in inner_from:
            neighbours.extend(multi_layout[level - 1][c] for c in outer_to)
        else:
            neighbours.append(multi_layout[level][n + neighbour_distance])

    if n == 12:
        return False

    neighbours = []
    append_neighbours(-1, outer_left, inner_left, inner_right, outer_right)  # Left neighbours
    append_neighbours(1, outer_right, inner_right, inner_left, outer_left)  # Right neighbours
    append_neighbours(-SIDE_SIZE, outer_top, inner_top, inner_bottom, outer_bottom)  # Top neighbours
    append_neighbours(SIDE_SIZE, outer_bottom, inner_bottom, inner_top, outer_top)  # Bottom neighbours

    infested_neighbours = sum(1 for cell in neighbours if cell == '#')
    return infested_neighbours == 1 or (infested_neighbours == 2 and multi_layout[level][n] != '#')


def iterate_layout(level, multi_layout):
    if level + 1 not in multi_layout or level - 1 not in multi_layout:
        return multi_layout[level]
    return ''.join(['#' if is_cell_on_level_infested(n, level, multi_layout) else '.' for n in range(0, LAYOUT_SIZE)])


def iterate_multi(multi_layout):
    return {level: iterate_layout(level, multi_layout) for level in multi_layout}


def count_bugs(multi_layout):
    return sum(1 for layout in multi_layout.values() for cell in layout if cell == '#')


def get_bugs_after_iterations(eris_raw, iterations):
    multi_layout = create_multi_layout(eris_raw, iterations)
    for i in range(iterations):
        multi_layout = iterate_multi(multi_layout)
    ret = count_bugs(multi_layout)
    return ret


def create_multi_layout(eris_raw, max_iterations):
    layout = parse_layout(eris_raw)
    empty_layout = '.' * LAYOUT_SIZE
    multi_layout = {0: layout}
    for i in range(1, max_iterations + 2):
        multi_layout[i] = empty_layout
        multi_layout[-i] = empty_layout
    return multi_layout


iterations_to_check = 200
bugs = get_bugs_after_iterations(read_data("24"), iterations_to_check)
print(f'After {iterations_to_check} iterations there are {bugs} bugs')  # 1963
