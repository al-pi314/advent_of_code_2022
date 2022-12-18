from collections import Counter, deque


def get_edges(cordinates):
    edges = []
    for i in range(len(cordinates)):
        for d in (-1, 1):
            edge_cordinates = cordinates[:]
            edge_cordinates[i] += d
            edges.append(tuple(edge_cordinates))
    return edges

def has_water_access(block, blocks, limits, memory):
    visited=set()
    q = deque([block])
    has_access = False
    while q:
        p = q.popleft()
        if p in visited:
            continue
        visited.add(p)

        if p in blocks:
            continue
        
        if p in memory and memory[p]:
            return True
        
        if any([p[i] <= limits[i][0] or p[i] >= limits[i][1] for i in range(len(p))]):
            has_access = True
            break

        q.extend(get_edges(list(p)))
    for p in visited:
        memory[p] = has_access
    return has_access        

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

    memory = {}
    print("Part 2:", sum([c for b, c in bordering_blocks.items() if has_water_access(b, blocks, limits, memory)]))