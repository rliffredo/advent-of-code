from typing import Tuple

import math

from common import read_data


def parse_map():
    lines = read_data('08', True)
    tree_map_r = [list(map(int, line)) for line in lines]
    tree_map_c = [list(sublist) for sublist in zip(*tree_map_r)]
    tree_map_d = {
        (x, y): int(c)
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    sizes = (0, len(lines) - 1) * 2
    return sizes, tree_map_r, tree_map_c, tree_map_d


def part_1() -> int:
    def is_visible(tree: Tuple[int, int]) -> bool:
        tree_x, tree_y = tree
        tree_height = tree_map_d[tree]
        current_row = tree_map_r[tree_y]
        current_column = tree_map_c[tree_x]
        return any((
            tree_x in (0, sizes[1]),  # edge
            tree_y in (0, sizes[3]),  # edge
            all(t < tree_height for t in current_row[:tree_x]),  # left
            all(t < tree_height for t in current_row[tree_x + 1:]),  # right
            all(t < tree_height for t in current_column[:tree_y]),  # top
            all(t < tree_height for t in current_column[tree_y + 1:]),  # bottom
        ))

    sizes, tree_map_r, tree_map_c, tree_map_d = parse_map()
    visible_trees = {
        tree
        for tree in tree_map_d
        if is_visible(tree)
    }
    return len(visible_trees)


def scenic_score(tree: Tuple[int, int], tree_maps) -> int:
    def lower_trees(trees) -> int:
        if not trees:
            return 0
        # If the view arrives until the edge, take all the trees, otherwise
        # take all the trees _plus_ the last tree
        for d, t in enumerate(trees):
            if t >= tree_height:
                return d + 1
        else:
            return len(trees)

    tree_map_r, tree_map_c, tree_map_d = tree_maps
    tree_x, tree_y = tree
    tree_height = tree_map_d[tree]
    t_left = list(reversed(tree_map_r[tree_y][:tree_x]))
    t_right = tree_map_r[tree_y][tree_x + 1:]
    t_up = list(reversed(tree_map_c[tree_x][:tree_y]))
    t_down = tree_map_c[tree_x][tree_y + 1:]

    return math.prod((
        lower_trees(t_left),
        lower_trees(t_right),
        lower_trees(t_down),
        lower_trees(t_up),
    ))


def part_2() -> int:
    sizes, *tree_maps = parse_map()
    scored_trees = {
        tree: scenic_score(tree, tree_maps)
        for tree in tree_maps[2]
    }
    return max(scored_trees.values())


SOLUTION_1 = 1672
SOLUTION_2 = 327180

if __name__ == '__main__':
    print(part_1())
    print(part_2())
