from functools import reduce

tree_heights = []
tree_visibilities = []
with open('input.txt') as f:
    for line in f:
        line = line.strip("\n")
        tree_heights.append(list(map(int, list(line))))
        tree_visibilities.append([False] * len(tree_heights[-1]))

def sweep(tree_visibilities, start, end, horizontal=False):
    step = 1 if start < end else -1
    max_height = [-1] * len(tree_heights) if horizontal else [-1] * len(tree_heights[0])

    visible_indices = set()
    for sweep_idx in range(start, end, step):
        for section_idx in range(len(max_height)):
            x, y = (sweep_idx, section_idx) if horizontal else (section_idx, sweep_idx)
            if tree_heights[y][x] > max_height[section_idx]:
                max_height[section_idx] = tree_heights[y][x]
                tree_visibilities[y][x] = True
                visible_indices.add((x, y))
    return visible_indices
            
top_down = sweep(tree_visibilities, 0, len(tree_heights), horizontal=False)
bottom_up = sweep(tree_visibilities, len(tree_heights) - 1, -1, horizontal=False)
left_right = sweep(tree_visibilities, 0, len(tree_heights[0]), horizontal=True)
right_left = sweep(tree_visibilities, len(tree_heights[0]) - 1, -1, horizontal=True)

visible = set.union(top_down, bottom_up, left_right, right_left)
print("Part 1:", len(visible))

def direction_score(x, y, dx, dy):
    x2, y2 = x + dx, y + dy
    local_score = 0
    while True:
        if x2 < 0 or x2 >= len(tree_heights[0]) or y2 < 0 or y2 >= len(tree_heights):
            break
        local_score += 1
      

        if tree_heights[y2][x2] >= tree_heights[y][x]:
            break
        x2 += dx
        y2 += dy
        
    return local_score

def scenic_score(x, y):
    score = 1

    score *= direction_score(x, y, 1, 0)
    score *= direction_score(x, y, -1, 0)
    score *= direction_score(x, y, 0, 1)
    score *= direction_score(x, y, 0, -1)

    return score
    
def best_scenic_score():
    best_score = 0
    for y in range(len(tree_heights)):
        for x in range(len(tree_heights[0])):
            score = scenic_score(x, y)
            best_score = max(score, best_score)
    return best_score

print("Part 2:", best_scenic_score())