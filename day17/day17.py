import numpy as np

# encoded by left offset, top offset right offset and bottom offset (looking from left top)
rock_types = [
    np.array([
        [True, True, True, True]
    ]),
    np.array([
        [False, True, False],
        [True, True, True],
        [False, True, False],
    ]),
    np.array([
        [True, True, True],
        [False, False, True],
        [False, False, True],
    ]),
    np.array([
        [True],
        [True],
        [True],
        [True],
    ]),
    np.array([
        [True, True],
        [True, True],
    ])
]

def move_gen():
    with open("input.txt", "r") as f:
        moves = list(map(lambda x: 1 if x == ">" else -1, list(f.read())))
    i = 0
    while True:
        yield moves[i]
        i = (i + 1) % len(moves)

def rock_gen():
    i = 0
    while True:
        yield i
        i = (i + 1) % len(rock_types)

def is_stopped(terrain, rock, position):
    y, x = position
    h, w = rock.shape

    return (terrain[y:y+h, x:x+w] & rock).any()

def set_rock(terrain, rock, position):
    y, x = position
    h, w = rock.shape

    terrain[y:y+h, x:x+w] |= rock
    return y + h - 1

def hash(terrain, max_y, n_top_rows, rock_type):
    terrain_hash = 0
    bottom = max(0, max_y - n_top_rows)
    print(bottom, bottom + n_top_rows)
    for i in range(bottom, bottom + n_top_rows):
        for j in range(1, 8):
            terrain_hash = terrain_hash | (terrain[i, j] << (i * 7 + j))
    return terrain_hash << 4 | rock_type

def check_memory(terrain, max_y, n_top_rows, rock_type, rocks_fallen):
    if max_y < n_top_rows:
        return None
    global memory
    terrain_hash = hash(terrain, max_y, n_top_rows, rock_type)
    if terrain_hash in memory:
        return memory[terrain_hash]
    memory[terrain_hash] = (max_y, rocks_fallen)
    return None

def simulate(terrain):
    max_y = 0
    rocks_fallen = 0
    unique = True
    while unique:
        rocks_fallen += 1
        rock_type = next(rocks)
        rock = rock_types[rock_type]
        position = [max_y + 4, 3]

        while True:
            move = next(moves)
            position[1] += move
            if is_stopped(terrain, rock, position):
                position[1] -= move

            position[0] -= 1
            if is_stopped(terrain, rock, position):
                position[0] += 1
                max_y = max(max_y, set_rock(terrain, rock, position))

                memo_result = check_memory(terrain, max_y, use_last_n_rows, rock_type, rocks_fallen)
                if memo_result is not None:
                    unique = False
                    prev_y, prev_rocks_fallen = memo_result
                    y_change = max_y - prev_y
                    rocks_per_change = rocks_fallen - prev_rocks_fallen
                break
    return max_y, rocks_fallen, y_change, rocks_per_change
# rocks and move continious generator
rocks = rock_gen()
moves = move_gen()

# terrain setup
terrain = np.zeros((4000, 9), dtype=bool)
terrain[:, 0] = True
terrain[:, -1] = True
terrain[0, :] = True
 
# memorisation based on last n rows of terrain
memory = {}
use_last_n_rows = 1000


max_y, rocks_fallen, y_change, rocks_per_change = simulate(terrain)
print("max_y:", max_y, "rocks_fallen:", rocks_fallen, "y_change:", y_change, "rocks_per_change:", rocks_per_change)

# after 2022
height_2022 = max_y + int((2022 - rocks_fallen) // rocks_per_change) * y_change
print("Part 1:", height_2022, "remaining rocks:", (2022 - rocks_fallen) % rocks_per_change)

# after 1000000000000
height_1000000000000 = max_y + int((1000000000000 - rocks_fallen) // rocks_per_change) * y_change
print("Part 2:", height_1000000000000, "remaining rocks:", (1000000000000 - rocks_fallen) % rocks_per_change)