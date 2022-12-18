from collections import Counter, deque


def get_edges(cordinates):
    edges = []
    for i in range(len(cordinates)):
        for d in (-1, 1):
            edge_cordinates = cordinates[:]
            edge_cordinates[i] += d
            edges.append(tuple(edge_cordinates))
    return edges

def has_water_access(block, blocks, limits, visited, with_access):
    if block in visited:
        return False
    visited.add(block)

    if block in blocks:
        return False
    
    if any([block[i] <= limits[i][0] or block[i] >= limits[i][1] for i in range(len(block))]):
        return True

    if block in with_access:
        return True

    for edge in get_edges(list(block)):
        if has_water_access(edge, blocks, limits, visited, with_access):
            with_access.add(block)
            return True
    return False

with open("input.txt") as file:
    blocks = set()
    bordering_blocks = Counter()
    limits = [(float("inf"), float("-inf")) for _ in range(3)]
    for line in file:
        cordinates = list(map(int, line.split(",")))
        blocks.add(tuple(cordinates))
        bordering_blocks.update(get_edges(cordinates))
        for i in range(len(cordinates)):
            limits[i] = (min(limits[i][0], cordinates[i]), max(limits[i][1], cordinates[i]))
        
    print("Part 1:", sum([c for b, c in bordering_blocks.items() if b not in blocks]))

    with_access = set()
    print("Part 2:", sum([c for b, c in bordering_blocks.items() if has_water_access(b, blocks, limits, set(), with_access)]))