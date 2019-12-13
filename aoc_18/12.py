padding = 50

initial_state = '.' * padding + \
                '###..###....####.###...#..#...##...#..#....#.##.##.#..#.#..##.#####..######....#....##..#...#...#.#' + \
                '.' * padding*2

growth_map = {
    '..#.#': '#',
    '###.#': '.',
    '#.#.#': '.',
    '.#.#.': '.',
    '##...': '#',
    '...##': '.',
    '.##.#': '.',
    '.#...': '#',
    '####.': '#',
    '....#': '.',
    '.##..': '#',
    '.####': '#',
    '..###': '.',
    '.###.': '#',
    '#####': '#',
    '..#..': '#',
    '#..#.': '.',
    '###..': '#',
    '#..##': '#',
    '##.##': '#',
    '##..#': '.',
    '.#..#': '#',
    '#.#..': '#',
    '#.###': '#',
    '#.##.': '#',
    '.....': '.',
    '.#.##': '#',
    '#...#': '.',
    '...#.': '#',
    '..##.': '#',
    '##.#.': '#',
    '#....': '.',
}

def next_generation(pots):
    next_pots = ['.', '.']
    for pot in range(3, len(pots)-2):
        next_pots.append(growth_map[pots[pot-3:pot+2]])
    next_pots.extend(['.', '.'])
    return ''.join(next_pots)

def grow_pots(initial_state, generations):
    pots = initial_state
    for _generation in range(generations):
        pots = next_generation(pots)
    return pots

def sum_pots(pots):
    plants = sum(
        a[0]-padding
        for a in enumerate(pots)
        if a[1] == '#'
    )
    return plants

generations = 20
print(f'After {generations} generations the result is {sum_pots(grow_pots(initial_state, generations))}')

######################

initial_zero_pot = padding

def next_generation_fast(pots):
    next_pots = ['.'] * 4
    for pot in range(3, len(pots)-2):
        next_pots.append(growth_map[pots[pot-3:pot+2]])
    next_pots.extend(['.'] * 4)
    zero_offset = 2
    return ''.join(next_pots), zero_offset

def trim_generation(pots):
    trimmed_left = '.' * 4 + pots.lstrip('.')
    trim_amount = len(pots) - len(trimmed_left)
    return trimmed_left, trim_amount

def grow_pots_fast(initial_state, initial_zero, generations):
    pots = initial_state
    zero = initial_zero
    previous_gen = initial_state
    generation = 0  # for degenerate case when generations is 0
    for generation in range(generations):
        pots, offset_generation = next_generation_fast(pots)
        zero += offset_generation
        pots, offset_trimming = trim_generation(pots)
        zero -= offset_trimming
        if pots == previous_gen:
            break
        previous_gen = pots
    if generation < generations-1:
        zero = zero + (offset_generation - offset_trimming) * (generations - generation) + 1
    return pots, zero

def sum_pots_fast(pots, offset):
    plants = sum(
        a[0]-offset
        for a in enumerate(pots)
        if a[1] == '#'
    )
    return plants

generations = 50000000000
print(f'After {generations} generations the result is {sum_pots_fast(*grow_pots_fast(initial_state, initial_zero_pot, generations))}')
