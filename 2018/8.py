# node:
#   - metadata: [int]
#   - children: [nodes]

data = open('input_8.txt').read()
from collections import namedtuple
TreeNode = namedtuple('TreeNode', 'children, metadata')

def fetch_node(numbers):
    n_children = numbers.pop()
    n_metadata = numbers.pop()
    child_nodes = [fetch_node(numbers) for _ in range(n_children)]
    metadata = [numbers.pop() for _ in range(n_metadata)]
    return TreeNode(metadata=metadata, children=child_nodes)

def build_tree(raw_data):
    parsed_data = list(map(int, data.split()))
    parsed_data.reverse()
    try:
        return fetch_node(parsed_data)
    except:
        return None


def sum_metadata(node):
    return sum(node.metadata) + sum(sum_metadata(child) for child in node.children)

tree = build_tree(data)

checksum = sum_metadata(tree)
print(f'The sum of all metadata entries is {checksum}')

#############

def node_value(node):
    if not node.children:
        return sum(node.metadata)
    child_to_sum = [node.children[i-1] for i in node.metadata if i <= len(node.children)]
    value = sum(node_value(child) for child in child_to_sum)
    return value

new_checksum = node_value(tree)
print(f'The value of the root node {new_checksum}')
