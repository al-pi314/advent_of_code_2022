import numpy as np


def add_line(grid, sx, sy, ex, ey, offset):
    # adjust offset
    if sx < offset:
        grid = np.hstack((np.zeros((grid.shape[0], offset - sx), dtype=bool), grid))
        offset = sx
    sx, ex = sx - offset, ex - offset

    # extend grid if needed
    if ex > grid.shape[1]:
        grid = np.hstack((grid, np.zeros((grid.shape[0], ex - grid.shape[1]), dtype=bool)))
    if ey > grid.shape[0]:
        grid = np.vstack((grid, np.zeros((ey - grid.shape[0], grid.shape[1]), dtype=bool)))

    # add rocks
    grid[sy:ey, sx:ex] = True
    return grid, offset

def add_rock(grid, line, xoffset):
    corners = map(lambda x: tuple(map(int, x)), map(lambda x: x.split(","), line.strip("\n").split(" -> ")))
    previous = next(corners)
    offset = previous[0] if xoffset is None else xoffset
    start_end = lambda s, e: (min(s, e), max(s, e) +1)
    for x, y in corners:
        sx, ex = start_end(int(previous[0]), int(x))
        sy, ey = start_end(int(previous[1]), int(y))
        grid, offset = add_line(grid, sx, sy, ex, ey, offset)
        previous = (x, y)
    return grid, offset

def rock_structures():
    grid = np.empty((0, 0), dtype=bool)
    xoffset = None
    with open("input.txt") as f:
        for line in f:
            grid, xoffset = add_rock(grid, line, xoffset)
    return grid, xoffset

def drop_sand(rock_system, sand_source, drops=0, overflowed=False):
    x, y = sand_source
    if x < 0 or x >= rock_system.shape[1] or y >= rock_system.shape[0]:
        if not overflowed:
            print("Part 1:", drops)
        return 0, True
    if rock_system[y, x]:
        return 0, overflowed
    down, overflowed = drop_sand(rock_system, (x, y + 1), drops, overflowed)
    left, overflowed= drop_sand(rock_system, (x - 1, y +1), drops + down, overflowed)
    right, overflowed= drop_sand(rock_system, (x + 1, y +1), drops + down + left, overflowed)
    rock_system[y, x] = True
    return down + left + right + 1, overflowed

# read input
rock_system, xoffset = rock_structures()

# edge heights
lh = np.argmax(rock_system[:, 0])
rh = np.argmax(rock_system[:, -1])

# bottom gaps
gaps = rock_system[-1, :] == False

# drop sand
sand_source = (500 - xoffset, 0)
drops, _ = drop_sand(rock_system, sand_source)

# new edge heights
nlh = np.argmax(rock_system[:, 0])
nrh = np.argmax(rock_system[:, -1])

# additional drops in left overflow
if nlh < lh:
    # out of system drops (from left to left)
    h = rock_system.shape[0] - nlh
    drops += (h * (h + 1)) // 2

    # in system drops (from left to right)
    for y in range(nlh, rock_system.shape[0]):
        d, _ = drop_sand(rock_system, (0, y), overflowed=True)
        drops += d

# additional drops in right overflow
if nrh < rh:
    # out of system drops (from right to right)
    h = rock_system.shape[0] - nrh
    drops += (h * (h + 1)) // 2

    # in system drops (from right to left)
    for y in range(nrh, rock_system.shape[0]):
        d, _ = drop_sand(rock_system, (rock_system.shape[1] -1, y), overflowed=True)
        drops += d

# filled gaps
filled_gaps = [True] + list(gaps & (rock_system[-1, :] == True)) + [True]
neighbours = set()
for i in range(1, len(filled_gaps) -1):
    if not filled_gaps[i] and (filled_gaps[i -1] or filled_gaps[i +1]):
        neighbours.add(i)
drops += np.sum(filled_gaps) + len(neighbours) - 2

print("Part 2:", drops)