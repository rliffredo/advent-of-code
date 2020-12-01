from common import read_data, intcode, print_map


class SpaceDrone:

    def __init__(self):
        self.computer = intcode.IntCode(self.provide_input, self.collect_output)
        self.computer.load(read_data("19"))
        self.computer.snapshot()
        self.x = 0
        self.y = 0
        self.spacemap = {}
        self.input_direction = False
        self.range_x = (0, 0)
        self.range_y = (0, 0)

    def run(self, range_x, range_y):
        self.range_x = range_x
        self.range_y = range_y
        for self.y in range(*self.range_y):
            for self.x in range(*self.range_x):
                if (self.x, self.y) not in self.spacemap:
                    self.computer.restore_snapshot()
                    self.computer.execute()

    def collect_output(self, value):
        self.spacemap[self.x, self.y] = value

    def provide_input(self):
        self.input_direction = not self.input_direction
        return self.x if self.input_direction else self.y


################
# ## PART 1 ## #
################

def affected_zones():
    sd = SpaceDrone()
    sd.run((0, 50), (0, 50))
    print_map((0, 49, 0, 49), lambda x, y: '#' if sd.spacemap[x, y] else ' ')
    return sum(sd.spacemap.values())


print(f'Number of affected zones: {affected_zones()}')  # 223


################
# ## PART 2 ## #
################

def is_hundred_corner(x, y, drone, print_sums=False):
    drone.run((x - 1, x + 100), (y - 1, y + 1))
    drone.run((x - 1, x + 1), (y - 1, y + 100))
    sum_x_at_y = sum(drone.spacemap[mx, y] for mx in range(x, x + 100))
    sum_y_at_x = sum(drone.spacemap[x, my] for my in range(y, y + 100))
    if print_sums:
        print(f'At point {(x, y)} we have {sum_y_at_x} in x and {sum_x_at_y} in y')
    return sum_y_at_x >= 100 and sum_x_at_y >= 100


def find_corner():
    sd = SpaceDrone()
    x, y = find_candidate(sd)
    x, y = find_from_candidate(sd, x, y)
    return x, y


def find_from_candidate(sd, x, y):
    ix, iy = 0, 0
    while (ix, iy) != (x, y):
        ix, iy = x, y
        while is_hundred_corner(x, y, sd, False):
            x = x - 1
            y = y - 1
        x = x + 1
        y = y + 1
        while is_hundred_corner(x, y, sd, False):
            y = y - 1
        y = y + 1
        while is_hundred_corner(x, y, sd, False):
            x = x - 1
        x = x + 1
    return x, y


def find_candidate(sd):
    """
    Find an initial candidate using a simple heuristic
    from the shape of the solution of phase 1
    """
    for x in range(700, 1200):
        y = int(x * 0.8)
        if is_hundred_corner(x, y, sd, False):
            return x, y


leftmost, topmost = find_corner()
print(f'The topleft corner hosting a 100-square has code {leftmost * 10000 + topmost}')  # 9480761
