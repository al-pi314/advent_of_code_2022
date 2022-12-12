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

def can_climb(y, x, y2, x2):
    return grid[y2][x2] - grid[y][x] <= 1

def queue_adder(q, steps):
    def add(y, x, dy, dx):
        ny, nx = y + dy, x + dx
        in_bounds = (ny >= 0 and ny < len(grid) and nx >= 0 and nx < len(grid[0]))
        if in_bounds and can_climb(y, x, ny, nx):
            q.append(((ny, nx), steps))
    return add

def climb(start, least_moves):
    front = deque()
    front.append((start, 0))

    while len(front) > 0:
        (y, x), steps = front.popleft()
        
        if (y, x) in least_moves and least_moves[(y, x)] <= steps:
            continue
        least_moves[(y, x)] = steps
        
        if (y, x) == finish:
            return steps
        
        add_to_queue = queue_adder(front, steps + 1)
        add_to_queue(y, x, -1, 0)
        add_to_queue(y, x, 1, 0)
        add_to_queue(y, x, 0, -1)
        add_to_queue(y, x, 0, 1)
        
    return float('inf')

# Part 1
least_moves = {}
best_start_steps = climb(start, least_moves)
print("Part 1:", best_start_steps)

# Part 2
for a_start in a_starts:
    best_start_steps = min(best_start_steps, climb(a_start, least_moves))
print("Part 2:", best_start_steps)