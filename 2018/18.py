from collections import namedtuple
import math


def read_data():
    data = open('input_18.txt').readlines()
    data = [line.strip('\n') for line in data]
    return data


Point = namedtuple('Point', 'x, y')


def parse_data(data):
    area = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            p = Point(x, y)
            area[p] = char
    return area


def changed_area(area, minute):
    return {p: changed_acre(p, area, minute) for p in area}


def changed_acre(p, area, minute):
    grounds, trees, lumbers = count_neighbours(p, area)
    current_state = area[p]
    new_state = current_state
    if current_state == '.' and trees >= 3:
        new_state = '|'
    if current_state == '|' and lumbers >= 3:
        new_state = '#'
    if current_state == '#' and not (lumbers >= 1 and trees >= 1):
        new_state = '.'
    # print(f'[{minute}] {(grounds, trees, lumbers)}: {current_state} -> {new_state}')
    return new_state


def count_neighbours(p, area):
    grounds = 0
    trees = 0
    lumbers = 0
    for x in range(p.x - 1, p.x + 2):
        for y in range(p.y - 1, p.y + 2):
            if x == p.x and y == p.y:
                continue
            n = Point(x, y)
            if n not in area:
                continue
            grounds += 1 if area[n] == '.' else 0
            trees += 1 if area[n] == '|' else 0
            lumbers += 1 if area[n] == '#' else 0
    return grounds, trees, lumbers


def print_area(area):
    size = int(math.sqrt(len(area)))
    table = [
        ['.' for _x in range(size)]
        for _y in range(size)
    ]
    for block in area:
        table[block.y][block.x] = area[block]
    lines = []
    for i, line in enumerate(table):
        lines.append(''.join(c for c in line))
    res = '\n'.join(lines) + '\n'
    print(res)


def play(area, minutes):
    new_area = area
    # print_area(area)
    for minute in range(minutes):
        new_area = changed_area(new_area, minute)
        # print_area(new_area)
        # input()
    return new_area


def count_resource_value(area):
    trees = sum(1 for p in area if area[p] == '|')
    lumbers = sum(1 for p in area if area[p] == '#')
    return trees, lumbers


data = read_data()
area = parse_data(data)
final_area = play(area, 10)
trees, lumbers = count_resource_value(final_area)
print(f'After 10 minutes, there are {trees} trees and {lumbers} lumberyards, for a total count of {trees * lumbers}')


######

# 178942 too low
def areastr(area):
    return ''.join(area.values())


def play_memoized(area, minutes):
    areas = {}
    new_area = area
    area_bmp = areastr(new_area)
    print_area(area)
    for minute in range(minutes):
        areas[area_bmp] = minute
        new_area = changed_area(new_area, minute)
        area_bmp = areastr(new_area)
        if area_bmp in areas:
            return areas, areas[area_bmp], minute + 1
    return areas, None, None


data = read_data()
area = parse_data(data)
all_areas, first_appearance, next_appearance = play_memoized(area, 1000000000)
cycle_time = next_appearance - first_appearance
n = first_appearance
while n < 1000000000:
    n += cycle_time
n -= cycle_time
m = 1000000000 - n
s = first_appearance + m
s_areas = [area for area in all_areas if all_areas[area] == s]
s_area = s_areas[0]


def count_resource_value_str(area_str):
    trees = sum(1 for p in area_str if p == '|')
    lumbers = sum(1 for p in area_str if p == '#')
    return trees, lumbers


trees, lumbers = count_resource_value_str(s_area)
print(
    f'After 1000000000 minutes, there are {trees} trees and {lumbers} lumberyards, for a total count of {trees * lumbers}')
