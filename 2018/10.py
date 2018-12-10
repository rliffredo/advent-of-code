# position=< 43754, -54319> velocity=<-4,  5>

def parse(line):
    m = re.match('position=<([- ]?\d+), ([- ]?\d+)> velocity=<([- ]?\d), ([- ]?\d)>', line)
    try:
        return tuple(map(int, m.groups()))
    except:
        print(line)
        raise

data = open('input_10.txt').readlines()
initial_position = [parse(d) for d in data]

def next_point_position(point):
    return (point[0]+point[2], point[1]+point[3], point[2], point[3])

def next_position(position):
    return [next_point_position(p) for p in position]

def get_rect(position):
    max_x = max(position, key=lambda p: p[0])[0]
    min_x = min(position, key=lambda p: p[0])[0]
    max_y = max(position, key=lambda p: p[1])[1]
    min_y = min(position, key=lambda p: p[1])[1]
    return min_x, min_y, max_x, max_y

def get_size(position):
    min_x, min_y, max_x, max_y = get_rect(position)
    dx = max_x - min_x
    dy = max_y - min_y
    return abs(dx*dy), abs(dx), abs(dy)

def evolve_position(position, max_iterations):
    last_size, dx, dy = get_size(position)
    sizes = []
    for iteration_count in range(max_iterations):
        position = next_position(position)
        size, dx, dy = get_size(position)
        sizes.append((iteration_count, size, dx, dy))
        if size<10000 and dx<600 and dy<30:
            print(f'\n*********************\nIteration {iteration_count}\n*********************\n')
            print_position(position)
            # return iteration_count, position, sizes
    else:
        return iteration_count, position, sizes

def get_best(sizes):
    return min(sizes, lambda s: s[1])

def print_position(position):
    min_x, min_y, max_x, max_y = get_rect(position)
    skymap = [['.'] * (abs(max_x-min_x)+1) for _ in range((abs(max_y-min_y)+1))]
    try:
        for point in position:
            assert min_x <= point[0] <= max_x
            assert min_y <= point[1] <= max_y
            skymap[point[1]-min_y][point[0]-min_x] = '#'
    except:
        print('############')
        print(point)
    for row in skymap:
        print(''.join(row))
    return skymap


