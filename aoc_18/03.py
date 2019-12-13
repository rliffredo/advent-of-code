import re
from collections import Counter

def parse(line):
    m = re.match('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    try:
        return tuple(map(int, m.groups()))
    except:
        print(line)
        raise

def make_areas(claim):
    return [(x, y)
    for x in range(claim[1], claim[1]+claim[3])
    for y in range(claim[2], claim[2]+claim[4])]


data = open('input_03.txt').readlines()
parsed = [parse(d) for d in data]
total_counter = Counter()

for claim in parsed:
    area = make_areas(claim)
    total_counter.update(area)

overlapping = [area for area in total_counter if total_counter[area] > 1]
print(f'All overlapping areas: {len(overlapping)}')


###########


not_overlapping = {area for area in total_counter if total_counter[area] == 1}

for claim in parsed:
    areas = make_areas(claim)
    if not_overlapping.issuperset(areas):
        print(f'Patch without any overlaps: {claim[0]}')
