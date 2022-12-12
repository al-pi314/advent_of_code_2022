from collections import deque

grid = []
start = None
finish = None
a_starts = []
with open("input.txt") as f:
    for line in f:
        grid.append([])
        for c in line.strip():
            if c == 'S':
                start = ((len(grid) - 1, len(grid[-1])))
                c = 'a'
            elif c == 'E':
                finish = (len(grid) - 1, len(grid[-1]))
                c = 'z'
            elif c == 'a':
                a_starts.append((len(grid) - 1, len(grid[-1])))
            grid[-1].append(ord(c) - ord('a'))

def height_ok(y, x, dy, dx):
    return grid[y + dy][x + dx] - grid[y][x] <= 1


def climb(start, start_steps):
    front = deque()
    front.append((start, 0))
    visited = set()
    while len(front) > 0:
        (y, x), steps = front.popleft()
        if (y, x) in visited:
            continue
        if (y, x) in start_steps and start_steps[(y, x)] <= steps:
            return float('inf')
        visited.add((y, x))
        if (y, x) == finish:
            return steps
        if y > 0 and height_ok(y, x, -1, 0):
            front.append(((y - 1, x), steps + 1))
        if y < len(grid) - 1 and height_ok(y, x, 1, 0):
            front.append(((y + 1, x), steps + 1))
        if x > 0 and height_ok(y, x, 0, -1):
            front.append(((y, x - 1), steps + 1))
        if x < len(grid[y]) - 1 and height_ok(y, x, 0, 1):
            front.append(((y, x + 1), steps + 1))
    return float('inf')

start_steps = {start: climb(start, {})}
best_start_steps = start_steps[start]
print("Part 1:", best_start_steps)
for a_start in a_starts:
    start_steps[a_start] = climb(a_start, start_steps)
    best_start_steps = min(best_start_steps, start_steps[a_start])
print("Part 2:", best_start_steps)