from common import distance, read_data


def parse_data(program):
    return program[0].split(','), program[1].split(',')


def make_path_for_movement(start, steps, movement, path):
    direction = movement[0]
    amount = int(movement[1:])

    dx = 1 if direction == 'R' else -1 if direction == 'L' else 0
    dy = 1 if direction == 'U' else -1 if direction == 'D' else 0

    point = start
    for d in range(amount+1):
        point = (start[0] + d * dx, start[1] + d * dy)
        if point not in path:
            path[point] = steps
        steps += 1

    return point, steps-1


def make_full_path(wire):
    start = (0, 0, 0)
    steps = 0
    path = {}
    for movement in wire:
        arrival, walked_steps = make_path_for_movement(start, steps, movement, path)
        start = arrival
        steps = walked_steps
    points_in_path = set(path.keys())
    points_in_path.remove((0, 0))
    return points_in_path, path


def get_intersections(w1, w2):
    path1, distances1 = make_full_path(w1)
    path2, distances2 = make_full_path(w2)
    intersections = path1.intersection(path2)
    return intersections, distances1, distances2


def get_closest_intersection(intersections):
    distances = [distance((0, 0), i) for i in intersections]
    return min(distances)


def get_smallest_intersection(intersections, p1, p2):
    frequencies = []
    for i in intersections:
        f = p1[i] + p2[i]
        frequencies.append(f)
    return min(frequencies)


wire_data = parse_data(read_data('03'))
all_intersections, path1, path2 = get_intersections(*wire_data)
closest = get_closest_intersection(all_intersections)
print(f'Closest intersection was: {closest}')  # 227

smallest = get_smallest_intersection(all_intersections, path1, path2)
print(f'Smallest intersection was: {smallest}')  # 20286
