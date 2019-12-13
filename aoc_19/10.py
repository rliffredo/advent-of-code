import math
from fractions import Fraction

from common import read_data


def parse_spacemap(map_data):
    spacemap = {}
    for y, line in enumerate(map_data):
        for x, char in enumerate(line.strip()):
            spacemap[(x, y)] = char == '#'
    return spacemap


################
# ## PART 1 ## #
################

def los_map_for_point(space, center):
    los_map = {p: True for p in space}
    for p in space:
        if p == center:
            continue
        mark_covered(los_map, space, center, p)
    return los_map


def mark_covered(los_map, spacemap, center, point):
    if not spacemap[point]:
        # No asteroids here, so it will not cover anything
        return
    step_x, step_y = get_steps(center, point)
    point_analyzed = point
    while True:
        point_analyzed = (point_analyzed[0] + step_x, point_analyzed[1] + step_y)
        if point_analyzed in spacemap:
            los_map[point_analyzed] = False
        else:
            break


def get_steps(center, point):
    dx = point[0] - center[0]
    if dx == 0:
        return 0, -1 if center[1] > point[1] else 1
    dy = point[1] - center[1]
    ratio = Fraction(dy, dx)
    step_x = abs(ratio.denominator) * (-1 if center[0] > point[0] else 1)
    step_y = abs(ratio.numerator) * (-1 if center[1] > point[1] else 1)
    return step_x, step_y


def asteroids_in_los(spacemap, center, los_map):
    return [point for point in spacemap if spacemap[point] and los_map[point] and point != center]


def visibility_per_point(spacemap):
    all_los_maps = {p: los_map_for_point(spacemap, p) for p in spacemap if spacemap[p]}
    visible_asteroids_per_point = {p1: asteroids_in_los(spacemap, p1, los_map) for p1, los_map in all_los_maps.items()}
    visible_count_per_point = [(p, len(visible_asteroids_per_point[p])) for p in visible_asteroids_per_point]
    sorted_points = list(reversed(sorted(visible_count_per_point, key=lambda vp: vp[1])))
    return sorted_points


data = read_data('10', True)
points_and_visibility = visibility_per_point(parse_spacemap(data))
print(points_and_visibility[0])  # (23, 19), 278


################
# ## PART 2 ## #
################

def get_laser_target(station_position, max_map_size):
    aim_x = station_position[0]
    aim_y = 0
    direction = 'right'
    while True:
        assert 0 <= aim_x < max_map_size[0]
        assert 0 <= aim_y < max_map_size[1]
        yield aim_x, aim_y
        if direction == 'right':
            aim_x = aim_x + 1
            if aim_x == max_map_size[0] - 1:
                direction = 'down'
        elif direction == 'down':
            aim_y = aim_y + 1
            if aim_y == max_map_size[1] - 1:
                direction = 'left'
        elif direction == 'left':
            aim_x = aim_x - 1
            if aim_x == 0:
                direction = 'up'
        elif direction == 'up':
            aim_y = aim_y - 1
            if aim_y == 0:
                direction = 'right'


def first_target_in_los(spacemap, station, target_point):
    step_x, step_y = get_steps(station, target_point)
    point_in_laser_path = station
    while True:
        point_in_laser_path = (point_in_laser_path[0] + step_x, point_in_laser_path[1] + step_y)
        if point_in_laser_path not in spacemap:
            return None
        if spacemap[point_in_laser_path]:
            return point_in_laser_path


def get_angle(station, asteroid):
    """
    Proof that I need to get better at trigonometry
    """
    dx = (asteroid[0] - station[0])
    dy = (asteroid[1] - station[1])
    at = math.atan2(dy, dx)
    return at if at >= -math.pi / 2 else at + 2 * math.pi


def remove_asteroids(spacemap, station):
    asteroids_in_maps = sum(1 for p in spacemap.values() if p is True and p != station)
    asteroids_removed = 0
    while True:
        los_map = los_map_for_point(spacemap, station)
        removed_asteroids = sorted(asteroids_in_los(spacemap, station, los_map))
        if not removed_asteroids:
            print(f'** Removed {asteroids_removed} out of {asteroids_in_maps} **')
            break
        for asteroid in removed_asteroids:
            spacemap[asteroid] = False
        removed_with_angles = [(asteroid, get_angle(station, asteroid)) for asteroid in removed_asteroids]
        sorted_removed_with_angles = sorted(removed_with_angles, key=lambda a: a[1])
        for removed in sorted_removed_with_angles:
            asteroids_removed += 1
            print(f'Removed {asteroids_removed} - {removed}')
        if asteroids_removed == asteroids_in_maps:
            break


data = read_data('10', True)
remove_asteroids(parse_spacemap(data), (23, 19))
