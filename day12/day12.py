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

def add_to_queue(q, y, x, dy, dx, steps):
    ny = y + dy
    nx = x + dx
    if ny >= 0 and ny < len(grid) and nx >= 0 and nx < len(grid[0]) and height_ok(y, x, dy, dx):
        q.append(((ny, nx), steps))

def climb(start, least_moves):
    front = deque()
    front.append((start, 0))
    visited = set()
    while len(front) > 0:
        (y, x), steps = front.popleft()
        # prevernt cycles
        if (y, x) in visited:
            continue
        visited.add((y, x))
        
        # prevent worse path from current strat
        if (y, x) in least_moves and least_moves[(y, x)] <= steps:
            continue
        least_moves[(y, x)] = steps
        
        if (y, x) == finish:
            return steps
        
        add_to_queue(front, y, x, -1, 0, steps + 1)
        add_to_queue(front, y, x, 1, 0, steps + 1)
        add_to_queue(front, y, x, 0, -1, steps +1)
        add_to_queue(front, y, x, 0, 1, steps + 1)
    return float('inf')

least_moves = {}
best_start_steps = climb(start, least_moves)
print("Part 1:", best_start_steps)
for a_start in a_starts:
    start_steps = climb(a_start, least_moves)
    best_start_steps = min(best_start_steps, start_steps)
print("Part 2:", best_start_steps)