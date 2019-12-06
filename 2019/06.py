import networkx as nx

################
# ## PART 1 ## #
################

f = open('data/06.txt')
lines = f.readlines()
lines = [l.strip() for l in lines]
edges = [l.split(')') for l in lines]
orbits = nx.DiGraph()
orbits.add_edges_from(edges)

total_number = sum(len(nx.ancestors(orbits, orbit)) for orbit in orbits.nodes)
print(f'Total number of direct and indirect orbits: {total_number}')  # 251208

################
# ## PART 2 ## #
################

san = nx.ancestors(orbits, 'SAN')
you = nx.ancestors(orbits, 'YOU')
commons = san.intersection(you)
dy = you - commons
ds = san - commons

print(f'Minimum hops: {len(dy) + len(ds)}')  # 397
