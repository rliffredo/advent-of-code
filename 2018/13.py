from itertools import cycle

SIZE = 150
# SIZE = 7

class Cart:

    def __init__(self, cart_id, x, y, direction):
        assert 0 <= x < SIZE
        assert 0 <= x < SIZE
        assert direction in 'v^<>'
        self.cart_id = cart_id
        self.x = x
        self.y = y
        self.dir = direction

        self.next_dir = cycle('LSR')

    @property
    def coords(self):
        return (self.x, self.y) 
    
    def move(self, track):
        self.advance()
        self.update_direction(track)

    def advance(self):
        if self.dir == 'v':
            self.y += 1
        if self.dir == '^':
            self.y -= 1
        if self.dir == '>':
            self.x += 1
        if self.dir == '<':
            self.x -= 1
        assert 0 <= self.x < SIZE
        assert 0 <= self.x < SIZE

    def update_direction(self, track):
        if track[self.coords] == '+':
            self.dir = self.cross()
        elif track[self.coords] in '/\\':
            self.dir = self.turn(track[self.coords])

    def turn(self, curve_type):
        return {
            ('^', '\\'): '<',
            ('<', '\\'): '^',
            ('v', '\\'): '>',
            ('>', '\\'): 'v',
            ('^', '/'): '>',
            ('<', '/'): 'v',
            ('v', '/'): '<',
            ('>', '/'): '^',
        }[(self.dir, curve_type)]
    
    def cross(self):
        turn = next(self.next_dir)
        if turn == 'S':
            return self.dir
        return {
            ('^', 'L'): '<',
            ('<', 'L'): 'v',
            ('v', 'L'): '>',
            ('>', 'L'): '^',
            ('^', 'R'): '>',
            ('<', 'R'): '^',
            ('v', 'R'): '<',
            ('>', 'R'): 'v',
        }[(self.dir, turn)]

cart_id = 0
def get_tracks_and_carts(state):
    carts = []
    def cell_without_cart(x, y):
        global cart_id
        point = state[y][x]
        if point in 'v^<>':
            cart = Cart(cart_id, x, y, point)
            carts.append(cart)
            cart_id += 1
            return '-' if point in '<>' else '|'
        else:
            return point
    
    tracks = {(x, y): cell_without_cart(x, y)
              for x in range(SIZE)
              for y in range(SIZE)}
    
    return carts, tracks


def move_until_crash(carts, tracks):
    tick = 0
    while True:
        carts = sorted(carts, key=lambda c: (c.y, c.x))
        tick += 1
        cart_positions = set()
        for cart in carts:
            cart.move(tracks)
            if cart.coords in cart_positions:
                return cart.coords, tick  # Note that carts is now corrupted!
            else:
                cart_positions.add(cart.coords)


data = open('input_13.txt').readlines()
data = [line.strip('\n') for line in data]
carts, tracks = get_tracks_and_carts(data)
coords, tick = move_until_crash(carts, tracks)
print(f'First accident happened at tick #{tick} in {coords}')

###############

TICKS_TO_ANALYZE = [304]

def move_until_one(carts, tracks):
    tick = 0
    while True:
        carts = sorted(carts, key=lambda c: (c.y, c.x))
        tick += 1
        cart_collisions = []
        for cart in carts:
            cart.move(tracks)
            if cart.coords in {c.coords for c in carts if c.cart_id != cart.cart_id}:
                cart_collisions.append(cart.cart_id)
                collided = next(c for c in carts if c.coords == cart.coords and c.cart_id != cart.cart_id)
                cart_collisions.append(collided.cart_id)
        if cart_collisions:
            carts = [cart for cart in carts if cart.cart_id not in cart_collisions]
            if len(carts) == 1:
                return carts[0], tick

cart_id = 0
data = open('input_13.txt').readlines()
data = [line.strip('\n') for line in data]
carts, tracks = get_tracks_and_carts(data)
cart, tick = move_until_one(carts, tracks)
print(f'Last track at tick #{tick} is {cart.cart_id} in {cart.coords}')
