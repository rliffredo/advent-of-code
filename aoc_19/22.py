from time import process_time
from typing import Tuple

from common import read_data


def xgcd(a, b):
    """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def modinv(a, b):
    """return x such that (x * a) % b == 1"""
    g, x, _ = xgcd(a, b)
    if g == 1:
        return x % b


def calc(cp, a, m, size) -> int:
    return ((cp - a) * m) % size


def deal_new(stack_size, _n, _forward) -> Tuple[int, int]:
    return stack_size - 1, -1  # Result is the same, no matter the direction


def cut(_stack_size, n, forward) -> Tuple[int, int]:
    return n if forward else -n, 1


def deal_with_increment(stack_size, n, forward) -> Tuple[int, int]:
    return (0, n) if forward else (0, modinv(n, stack_size))


def parse_command(line):
    if 'cut' in line:
        command = cut
        param = int(line.split()[-1])
    elif 'increment' in line:
        command = deal_with_increment
        param = int(line.split()[-1])
    elif 'new stack' in line:
        command = deal_new
        param = None
    else:
        assert False, f"Not a command in input: [{line}]"
    return command, param


def calc_shuffler_params(commands, stack_size):
    global_m = 1
    global_a = 0
    for command in commands:
        a, m = command[0](stack_size, command[1], True)
        global_m = global_m * m
        global_a = global_a * m - a * m
    return global_a, global_m


def calc_unshuffler_params(commands, stack_size):
    global_m = 1
    global_a = 0
    for command in reversed(commands):
        a, m = command[0](stack_size, command[1], False)
        global_m = global_m * m
        global_a = global_a * m - a * m
    return global_a, global_m


################
# ## PART 1 ## #
################

def make_deck_shuffler(deck_size, commands):
    global_a, global_m = calc_shuffler_params(commands, deck_size)
    return lambda cp: (global_m * cp + global_a) % deck_size


def find_card():
    commands = [parse_command(line) for line in read_data("22", by_lines=True) if line and line.strip()]
    deck_shuffler = make_deck_shuffler(10_007, commands)
    position = deck_shuffler(2019)
    return position


print(f"After shuffling, card 2019 is at index {find_card()}")  # 1822


################
# ## PART 2 ## #
################

def make_deck_unshuffler(deck_size, commands, repetitions):
    global_a, global_m = calc_unshuffler_params(commands, deck_size)
    return lambda cp: ((global_m * cp + global_a) * repetitions) % deck_size


# -> rep 1
# (gm * cp + ga) % size
# -> rep 2
# ((gm * (((gm * cp + ga)) + ga) % size
# (gm^2 * cp + gm * ga + ga) % size
# rep 3
# (gm^2 * (gm * cp + ga) + gm * ga + ga) % size
# (gm^3 * cp + gm^2*ga + gm * ga + ga) % size

# -> rep 1
# (a*x + b) % size
# -> rep 2
# (a*(a*x + b) + b) % size
# (a^2*x + (a^1 + a^0)*b) % size
# rep 3
# (a^2*(a*x + b) + (a^1 + a^0)*b) % size
# (a^3*x + a^2*b + (a^1 + a^0)*b) % size
# (a^3*x + (a^2 + a^1 + a^0)*b) % size
# rep 4
# (a^3*(a*x + b) + (a^2 + a^1 + a^0)*b) % size
# (a^4*x +a^3*b) + (a^2 + a^1 + a^0)*b) % size
# (a^4*x +a^3*b + (a^2 + a^1 + a^0)*b) % size
# (a^4*x + (a^3 + a^2 + a^1 + a^0)*b) % size


# rep2(rep2)
# (a^2*(a^2*x + (a^1 + a^0)*b) + (a^1 + a^0)*b) % size
# (a^4*x + (a^3 + a^2)*b + (a^1 + a^0)*b) % size
# (a^4*x + (a^3 + a^2 + a^1 + a^0)*b) % size

def find_card_serious():
    commands = [parse_command(line) for line in read_data("22", by_lines=True) if line and line.strip()]
    deck_unshuffler = make_deck_unshuffler(119_315_717_514_047, commands, 101_741_582_076_661)
    value = deck_unshuffler(2020)
    return value


print(f"After shuffling a serious deck, card at index 2020 is {find_card_serious()}")  # XX 100049455231466 XX

# Result should be: 49174686993380


#
#
# from functools import partial, reduce
#
# # get modular multiplicative inverse for prime p
# def prime_modinv(p, mod):
#     return pow(p, mod - 2, mod)
#
# # get (a, b) coefficients for inverse linear index mapping functions ax+b
# def inverse_functions(instructions, ncards):
#     for line in reversed(instructions):
#         if line == 'deal into new stack':
#             yield -1, ncards - 1
#         elif line.startswith('cut'):
#             amount = int(line.split()[1])
#             yield 1, amount
#         else:
#             increment = int(line.split()[-1])
#             yield prime_modinv(increment, ncards), 0
#
# # compose linear functions ax+b and cx+d
# def compose(mod, f, g):
#     a, b = f
#     c, d = g
#     return c * a % mod, (c * b + d) % mod
#
# # repeat ax+b n times
# def repeat_linear(f, n, mod):
#     if n == 0:
#         return 1, 0
#     if n == 1:
#         return f
#     half, odd = divmod(n, 2)
#     g = repeat_linear(f, half, mod)
#     gg = compose(mod, g, g)
#     return compose(mod, f, gg) if odd else gg
#
# def card_at(index, ncards, nshuffles, instructions):
#     functions = inverse_functions(instructions, ncards)
#     invmap = reduce(partial(compose, ncards), functions, (1, 0))
#     a, b = repeat_linear(invmap, nshuffles, ncards)
#     return (index * a + b) % ncards
#
# instructions = read_data("22", by_lines=True)
# print(instructions)
# print(next(i for i in range(10007) if card_at(i, 10007, 1, instructions) == 2019))
# print(card_at(2020, 119315717514047, 101741582076661, instructions))
