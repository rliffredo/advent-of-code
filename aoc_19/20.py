import string
from collections import defaultdict

import networkx as nx

from common import read_data


def make_point(square_x, square_y):
    return square_x, square_y, 0


def make_floor_map(map_lines, can_walk):
    """
    General map with nodes and items
    TODO: move to common and refactor other exercises
    """

    def add_neighbours(square_x, square_y):
        if not can_walk(map_lines[square_y][square_x]):
            return
        if can_walk(map_lines[square_y - 1][square_x]):
            fm.add_edge(make_point(square_x, square_y), make_point(square_x, square_y - 1))
        if can_walk(map_lines[square_y + 1][square_x]):
            fm.add_edge(make_point(square_x, square_y), make_point(square_x, square_y + 1))
        if can_walk(map_lines[square_y][square_x - 1]):
            fm.add_edge(make_point(square_x, square_y), make_point(square_x - 1, square_y))
        if can_walk(map_lines[square_y][square_x + 1]):
            fm.add_edge(make_point(square_x, square_y), make_point(square_x + 1, square_y))

    fm = nx.Graph()
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if not can_walk(char):
                continue
            add_neighbours(x, y)

    return fm


def get_nearby_letter(node, text_map):
    if text_map[node[1] - 1][node[0]] in string.ascii_uppercase:
        return text_map[node[1] - 1][node[0]], make_point(node[0], node[1] - 1)
    if text_map[node[1] + 1][node[0]] in string.ascii_uppercase:
        return text_map[node[1] + 1][node[0]], make_point(node[0], node[1] + 1)
    if text_map[node[1]][node[0] - 1] in string.ascii_uppercase:
        return text_map[node[1]][node[0] - 1], make_point(node[0] - 1, node[1])
    if text_map[node[1]][node[0] + 1] in string.ascii_uppercase:
        return text_map[node[1]][node[0] + 1], make_point(node[0] + 1, node[1])
    return None, None


def is_inner_portal(l1_pos, min_x, min_y, max_x, max_y):
    return min_x < l1_pos[0] < max_x and min_y < l1_pos[1] < max_y


def tag_portals(text_map, donut):
    """
    A portal:
    - is a passage on the map
    - has an uppercase letter as neighbour in one direction
    - the name is given by the other uppercase letter as well
    - label name is top-bottom, left-right
    """
    min_x = min(n[0] for n in donut.nodes)
    min_y = min(n[1] for n in donut.nodes)
    max_x = max(n[0] for n in donut.nodes)
    max_y = max(n[1] for n in donut.nodes)
    for node in donut.nodes:
        l1, l1_pos = get_nearby_letter(node, text_map)
        if l1:
            l2, l2_pos = get_nearby_letter(l1_pos, text_map)
            assert l2
            name = ''.join(lx[1] for lx in sorted([(l1_pos, l1), (l2_pos, l2)]))
            donut.nodes[node]['portal'] = name
            portal_type = 'inner' if is_inner_portal(l1_pos, min_x, min_y, max_x, max_y) else 'outer'
            donut.nodes[node]['portal_type'] = portal_type


def get_steps(donut_map):
    portal_aa = next(n[0] for n in donut_map.nodes(data=True) if "portal" in n[1] and n[1]["portal"] == "AA")
    portal_zz = next(n[0] for n in donut_map.nodes(data=True) if "portal" in n[1] and n[1]["portal"] == "ZZ")
    return nx.shortest_path_length(donut_map, portal_aa, portal_zz)


################
# ## PART 1 ## #
################

def connect_portals(donut):
    portals = defaultdict(list)
    for node in donut.nodes(data=True):
        if node[1]:
            portals[node[1]['portal']].append(node[0])
    for portal_name in portals:
        if portal_name in ['AA', 'ZZ']:
            continue
        portal_nodes = portals[portal_name]
        assert len(portal_nodes) == 2
        donut.add_edge(portal_nodes[0], portal_nodes[1], portal=True)


def make_donut_map(text_map):
    donut = make_floor_map(text_map, lambda c: c == '.')
    tag_portals(text_map, donut)
    connect_portals(donut)
    return donut


################
# ## PART 2 ## #
################


def connect_multispace_portals(donut, outer_level, inner_level):
    portals_down = {node[1]['portal']: node[0]
                    for node in donut.nodes(data=True)
                    if node[0][2] == outer_level and node[1] and node[1]['portal_type'] == 'inner'}
    portals_up = {node[1]['portal']: node[0]
                  for node in donut.nodes(data=True)
                  if node[0][2] == inner_level and node[1] and node[1]['portal_type'] == 'outer'}

    assert len(portals_down) == len(portals_up)
    for portal_name in portals_up:
        donut.add_edge(portals_down[portal_name], portals_up[portal_name], portal=True)


def make_inner_space(donut, level):
    base_nodes = [node for node in donut.nodes(data=True) if node[0][2] == 0]
    for node in base_nodes:
        if 'portal' in node[1] and node[1]['portal'] in ['AA', 'ZZ']:
            continue  # Do not copy entrance and exit
        new_node = node_on_level(node[0], level)
        donut.add_node(new_node, **node[1])
    base_edges = [edge for edge in donut.edges(data=True) if edge[0][2] == 0 and edge[1][2] == 0]
    for edge in base_edges:
        node_1 = node_on_level(edge[0], level)
        node_2 = node_on_level(edge[1], level)
        donut.add_edge(node_1, node_2, **edge[2])


def node_on_level(node, level):
    node_x = node[0]
    node_y = node[1]
    node_z = level
    return node_x, node_y, node_z


def get_steps_multispace_donut_map(text_map):
    donut = make_floor_map(text_map, lambda c: c == '.')
    tag_portals(text_map, donut)

    for i in range(1, 100):
        make_inner_space(donut, i)
        connect_multispace_portals(donut, i - 1, i)
        try:
            return get_steps(donut)
        except nx.NetworkXNoPath:
            pass
    else:
        return -1


print(f'To go from AA to ZZ we need {get_steps_multispace_donut_map(read_data("20", by_lines=True))} steps')  # 6292
