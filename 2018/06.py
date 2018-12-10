from collections import namedtuple, defaultdict

Point = namedtuple('Point', 'x, y')

def parse_line(line):
    numbers = [int(n) for n in line.split(',')]
    return Point(x=numbers[0], y=numbers[1])

data = open('input_06.txt').readlines()
coordinates = [parse_line(line) for line in data]

max_x = max(coordinates, key=lambda p: p.x).x
max_y = max(coordinates, key=lambda p: p.y).y

# Get all areas
def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def get_nearest_coordinate(point_to_evaluate, coordinates):
    min_d = max_x + max_y + 1
    npoints_at_min_d = 0
    for coordinate in coordinates:
        d = distance(coordinate, point_to_evaluate)
        if d < min_d:
            ret_coord = coordinate
            min_d = d
            npoints_at_min_d = 1
        elif d == min_d:
            npoints_at_min_d += 1
    return ret_coord if npoints_at_min_d == 1 else None

areas = defaultdict(list)
for x in range(0, max_x):
    for y in range(0, max_y):
        point_to_evaluate = Point(x=x, y=y)
        coordinate = get_nearest_coordinate(point_to_evaluate, coordinates)
        if coordinate:
            areas[coordinate].append(point_to_evaluate)

# Remove infinite areas
def is_point_internal(point):
    return 0 < point.x < max_x-1 and 0 < point.y < max_y-1

def is_finite(area):
    return all(is_point_internal(p) for p in area)

finite_areas = [area for area in areas.values() if is_finite(area)]

# Get max area
max_area = max(finite_areas, key=len)

print(f'Largest area: {len(max_area)}')


#########

def distance_from_all_coordinates(x, y, coordinates):
    point_to_evaluate = Point(x=x, y=y)
    return sum(distance(point_to_evaluate, coordinate) for coordinate in coordinates)

distances = [
    distance_from_all_coordinates(x, y, coordinates)
    for x in range(0, max_x)
    for y in range(0, max_y)
]

region = [d for d in distances if d<10000]

print(f'Size of region with max distance <10000: {len(region)}')