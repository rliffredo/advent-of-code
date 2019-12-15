import math
from collections import Counter


################
# ## PART 1 ## #
################
from common import read_data, print_map


def split_by_layers(digits, width, height):
    layer_size = width * height
    layers = [digits[i:i + layer_size] for i in range(0, len(digits), layer_size)]
    return layers


def get_checksum(layers):
    dc = [Counter(l) for l in layers]
    sdc = sorted(dc, key=lambda x: x["0"])
    return sdc[0]["1"] * sdc[0]["2"]


WIDTH = 25
HEIGHT = 6

digits = read_data('08')

layers = split_by_layers(digits, WIDTH, HEIGHT)
print(f"Checksum is {get_checksum(layers)}")   # 2210


################
# ## PART 2 ## #
################

def render_layer(layer_digits, width):
    img = {}
    for p, d in enumerate(layer_digits):
        img[(p % width, math.floor(p/width))] = d
    return img


def merge_layer(img, width, height, layer_image):
    for x in range(width):
        for y in range(height):
            if img[(x, y)] == "2":
                img[(x, y)] = layer_image[(x, y)]


def stack_layers(image_layers, width, height):
    img = render_layer("2" * 150, width)
    for l in image_layers:
        layer_image = render_layer(l, width)
        merge_layer(img, width, height, layer_image)
    return img


def color(p):
    return 'X' if p == '1' else ' ' if p == '0' else '&'


def print_image(img, width, height):
    print_map((0, width-1, 0, height-1), lambda x, y: color(img[(x, y)]))


image = stack_layers(layers, WIDTH, HEIGHT)
print('')
print_image(image, WIDTH, HEIGHT)  # CGEGE
