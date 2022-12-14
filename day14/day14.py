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

def drop_sand(rock_system, sand_source):
    x, y = sand_source
    if x < 0 or x >= rock_system.shape[1] or y >= rock_system.shape[0] -1:
        return False
    if not rock_system[y +1, x]:
        return drop_sand(rock_system, (x, y + 1))
    elif not rock_system[y +1, x -1]:
        return drop_sand(rock_system, (x - 1, y +1))
    elif not rock_system[y +1, x +1]:
        return drop_sand(rock_system, (x + 1, y +1))
    elif rock_system[y, x]:
        return False
    rock_system[y, x] = True
    return True

rock_system, xoffset = rock_structures()

# add_floor = False # Part 1
# add_floor = True # Part 2
add_floor = True
if add_floor:
    xoffset -= rock_system.shape[0]
    rock_system = np.hstack((np.zeros((rock_system.shape[0], rock_system.shape[0]), dtype=bool), rock_system, np.zeros((rock_system.shape[0], rock_system.shape[0]), dtype=bool)))
    rock_system = np.vstack((rock_system, np.zeros((1, rock_system.shape[1]), dtype=bool), np.ones((1, rock_system.shape[1]), dtype=bool)))

drops = 0
sand_source = (500 - xoffset, 0)
while drop_sand(rock_system, sand_source):
    drops += 1
print(f'Dropped {drops} - {"Part 1" if not add_floor else "Part 2"}')