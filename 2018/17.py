import re
from collections import namedtuple

def read_data():
    data = open('input_17.txt').readlines()
    data = [d.strip() for d in data]
    return data

class GroundScan(dict):
    @property
    def min_x(self):
        if not '_min_x' in self:
            self['_min_x'] = min(pos.x for pos in self.keys() if isinstance(pos, Point)) - 10
        return self['_min_x']
    @property
    def max_x(self):
        if not '_max_x' in self:
            self['_max_x'] = max(pos.x for pos in self.keys() if isinstance(pos, Point)) + 10
        return self['_max_x']
    @property
    def min_y(self):
        return 0
    @property
    def clay_min_y(self):
        return min(pos.y for pos in self.keys() if isinstance(pos, Point) and self[pos]=='#')
    @property
    def max_y(self):
        if not '_max_y' in self:
            self['_max_y'] = max(pos.y for pos in self.keys() if isinstance(pos, Point))
        return self['_max_y']
    
    def is_in_box(self, point):
        if not isinstance(point, Point):
            return False
        return self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y
    
    def is_wall(self, point):
        if not isinstance(point, Point):
            return False
        return point in self and self[point] == '#'
    
    def is_water(self, point):
        if not isinstance(point, Point):
            return False
        return point in self and self[point] in '|~'
    
    def is_overflowing(self, point):
        if not isinstance(point, Point):
            return False
        return point in self and self[point] == '|'

    def print(self):
        table = [
            ['.' for _x in range(self.max_x+1 - self.min_x)]
            for _y in range(self.max_y+1 - self.min_y)
        ]
        for block in self:
            if not isinstance(block, Point):
                continue
            table[block.y - self.min_y][block.x - self.min_x] = self[block]
        lines = []
        for i, line in enumerate(table):
            lines.append(''.join(c for c in line))
        res = '\n'.join(lines) + '\n'
        print(res)


def parse_data(data):
    ground = GroundScan()
    for line in data:
        m = re.match('([xy])=(\d+), [xy]=(\d+)\.\.(\d+)', line)
        clay_blocks = _clay_coords(vertical=m.groups()[0]=='x',
                                   position=int(m.groups()[1]),
                                   start=int(m.groups()[2]), end=int(m.groups()[3]))
        for block in clay_blocks:
            ground[block] = '#'
    return ground


Point = namedtuple('Point', 'x, y')

def _clay_coords(vertical, position, start, end):
    return [Point(position, n) if vertical else Point(n, position) for n in range(start, end+1)]


def add_water(ground):
    start_pos = Point(500, 0)
    flow_from_point(ground, start_pos)
    ground[start_pos] = '+'


def can_flood(ground, point):
    # cannot flood
    #  - if it is falling on a overflowing left or right
    platform = Point(point.x, point.y+1)
    if not ground.is_in_box(platform):
        return False
    left = platform
    # TODO
    while ground.is_water(left):
        left = Point(left.x-1, left.y)
        if ground.is_overflowing(left):
            return False
    right = platform
    while ground.is_water(right):
        right = Point(right.x+1, right.y)
        if ground.is_overflowing(right):
            return False
    return True

    return True
    left = Point(point.x-1, point.y)
    right = Point(point.x+1, point.y)
    down = Point(point.x, point.y+1)
    if ground.is_water(down):
        return not (ground.is_water(left) or ground.is_water(right))
    return True

def flow_from_point(ground, point):
    drop_line = drop_water(ground, point)
    while drop_line:
        drop_place = drop_line.pop()
        if not can_flood(ground, drop_place):
            return
        l, r = flood(ground, drop_place)
        if l != r:
            if not ground.is_wall(l):
                flow_from_point(ground, l)
            if not ground.is_wall(r):
                flow_from_point(ground, r)
        if not can_water_rise(ground, drop_place):
            return

def can_water_rise(ground, point):
    left = point
    while ground.is_water(left):
        left = Point(left.x-1, left.y)
    right = point
    while ground.is_water(right):
        right = Point(right.x+1, right.y)
    return ground.is_wall(left) and ground.is_wall(right)

def drop_water(ground, start_pos):
    pos = start_pos
    drops = []
    while ground.is_in_box(pos) and not ground.is_wall(pos) and not ground.is_water(pos):
        ground[pos] = '|'
        drops.append(pos)
        pos = Point(pos.x, pos.y+1)
    return drops

def _can_continue_flooding(ground, position):
    if ground.is_wall(position):
        return False
    if ground.is_overflowing(position):
        return False
    platform = Point(position.x, position.y+1)
    if not ground.is_in_box(platform):
        return False
    if ground.is_wall(platform):
        return True
    if ground.is_water(platform):
        return can_flood(ground, position)
    return False

def flood(ground, start_pos):
    # fill right
    right_boundary = Point(start_pos.x+1, start_pos.y)
    while _can_continue_flooding(ground, right_boundary):
        ground[right_boundary] = '~'
        right_boundary = Point(right_boundary.x+1, right_boundary.y)
    # fill left
    left_boundary = Point(start_pos.x-1, start_pos.y)
    while _can_continue_flooding(ground, left_boundary):
        ground[left_boundary] = '~'
        left_boundary = Point(left_boundary.x-1, left_boundary.y)
    # fill point
    ground[start_pos] = '~'
    return left_boundary, right_boundary

def count_water(ground):
    min_y = ground.clay_min_y
    return sum(1 for p in ground if ground.is_water(p) and p.y >= min_y)

data = read_data()
ground = parse_data(data)
print(f'Parsed ground from {ground.min_x} to {ground.max_x}, with depth {ground.max_y}')
add_water(ground)
ground.print()
water = count_water(ground)
print(f'Total water in the ground is {water}')

#################

def is_water_at_rest(ground, point):
    if not ground.is_water(point):
        return False
    left = point
    while ground.is_water(left):
        if ground.is_overflowing(left):
            return False
        left = Point(left.x-1, left.y)
    right = point
    while ground.is_water(right):
        if ground.is_overflowing(right):
            return False
        right = Point(right.x+1, right.y)
    return True

def paint_flowing_water(ground):
    for point in ground:
        if not isinstance(point, Point):
            continue
        if ground.is_water(point) and not is_water_at_rest(ground, point):
            ground[point] = '|'


def count_water_at_rest(ground):
    return sum(1 for p in ground if ground.is_water(p) and not ground.is_overflowing(p))

paint_flowing_water(ground)
water_at_rest = count_water_at_rest(ground)
print(f'Total water reamining in the ground is {water_at_rest}')
