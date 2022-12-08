
from collections import deque


def read_creates(line):
    crates = []
    for i in range(1, len(line), 4):
        if line[i] == " ":
            crates.append(None)
            continue
        crates.append(line[i])
    return crates

def add_line_to_stack(crates, stacks):
    for i, crate in enumerate(crates):
        if crate is None:
            continue
        stacks[i].append(crate)

def read_move(line):
    p = line.split(" ")
    return int(p[1]), int(p[3]) -1, int(p[5])-1

def move_crates(n, froms, tos, stacks):
    # move n crates from froms to tos one by one
    for _ in range(n):
        stacks[tos].appendleft(stacks[froms].popleft())

def move_batch(n, froms, tos, stacks):
    # move n crates from froms to tos all at once
    batch = deque()
    for _ in range(n):
        batch.append(stacks[froms].popleft())
    stacks[tos] = batch + stacks[tos]


# crane_move_mode = move_crates # Part 1
# crane_move_mode = move_batch # Part 2
crane_move_mode = move_batch

with open("input.txt", "r") as f:
    # read first line seperatly to get number of stacks
    c = read_creates(f.readline())
    stacks = [deque() for _ in range(len(c))]

    # read other lines and add to stacks
    for line in f:
        if line == "\n":
            break
        add_line_to_stack(c, stacks)
        c = read_creates(line)

    # move crates
    for line in f:
        n, froms, tos = read_move(line)
        crane_move_mode(n, froms, tos, stacks)
    
    # print top crate of each stack
    for stack in stacks:
        print(stack[0] if stack else "0", end="")
    print()
    