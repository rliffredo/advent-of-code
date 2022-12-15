import re
from typing import Iterable

from common import read_data, distance


class Sensor:
    def __init__(self, line: str):
        coords = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line).groups()
        self.pos = int(coords[0]), int(coords[1])
        self.beacon = int(coords[2]), int(coords[3])
        self.beacon_distance = distance(self.pos, self.beacon)

    def is_point_in_range(self, point):
        return distance(self.pos, point) <= self.beacon_distance

    def __repr__(self):
        return f'S{self.pos}/B{self.beacon}/{self.beacon_distance}'


def parse_data():
    return [Sensor(line) for line in read_data('15', True) if line]


def part_1() -> int:
    def sensor_scan_width_at_row(sensor, row_y):
        scan_width = sensor.beacon_distance - abs(sensor.pos[1] - row_y) + 1
        return range(sensor.pos[0] - scan_width, sensor.pos[0] + scan_width)

    sensors = parse_data()
    y = 2_000_000

    coverage_at_row = {
        (x, y)
        for sensor in sensors
        for x in sensor_scan_width_at_row(sensor, y)
        if sensor.is_point_in_range((x, y))
    }
    beacons_in_row = {s.beacon for s in sensors if s.beacon[1] == y}
    return len(coverage_at_row - beacons_in_row)


def get_sensor_scan_border(sensor, max_dist) -> Iterable[tuple[int, int]]:
    def get_border_points(n):
        return [
            (sensor.pos[0] + n, sensor.pos[1] + sensor.beacon_distance - n + 1),
            (sensor.pos[0] + n, sensor.pos[1] - sensor.beacon_distance - n + 1),
            (sensor.pos[0] + sensor.beacon_distance - n + 1, sensor.pos[1] + n),
            (sensor.pos[0] - sensor.beacon_distance - n + 1, sensor.pos[1] + n),
        ]

    return (
        p
        for n in range(sensor.beacon_distance)
        for p in get_border_points(n)
        if 0 <= p[0] <= max_dist and 0 <= p[1] <= max_dist
    )


def part_2() -> int:
    """
    We know there is only ONE point in the desired area; hence it must be right
    on the boundary of at least one sensor.
    """
    sensors = parse_data()
    max_dist = 4_000_000
    return next(
        point[0] * 4_000_000 + point[1]
        for sensor in sensors
        for point in get_sensor_scan_border(sensor, max_dist)
        if not any(sensor.is_point_in_range(point) for sensor in sensors)
    )


SOLUTION_1 = 5112034
SOLUTION_2 = 13172087230812

if __name__ == '__main__':
    print(part_1())
    print(part_2())
