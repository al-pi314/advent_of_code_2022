import numpy as np

# adjust for your input
MEMORISE_LAST_N = 20 # if this is too low, false loop might be found
TERRAIN_SPACE = 5000 # if this is too low, loop won't be found and error will be returned

# simulate n rocks falling
PART_1 = 2022
PART_2 = 1000000000000

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

def hash(terrain, max_y, rock_type):
    terrain_hash = terrain[max_y - MEMORISE_LAST_N:max_y + 1, 1:8].tobytes()
    return terrain_hash + bytes([rock_type])

def check_memory(memory, terrain, rock_type, max_y, rocks_fallen):
    if max_y < MEMORISE_LAST_N:
        return None
    terrain_hash = hash(terrain, max_y, rock_type)
    if terrain_hash in memory:
        return memory[terrain_hash]
    memory[terrain_hash] = (max_y, rocks_fallen)
    return None

def repeats_until(until, y, rocks_fallen, y_change, rocks_per_change):
    total_y = y + int((until - rocks_fallen) // rocks_per_change) * (y_change)
    remaining_rocks = (until - rocks_fallen) % rocks_per_change
    return total_y, remaining_rocks

def simulate(terrain):
    use_memory = True
    memory = {}

    max_y = 0
    loop_y = 0
    rocks_fallen = 0
    while True:
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
                break
        
        if use_memory:
            # try to find a loop
            m = check_memory(memory, terrain, rock_type, max_y, rocks_fallen)
            if m is not None:
                prev_max_y, prev_rocks_fallen = m
                y_change = max_y - prev_max_y
                rocks_per_change = rocks_fallen - prev_rocks_fallen
                
                p1_y, p1_remaining = repeats_until(PART_1, max_y, rocks_fallen, y_change, rocks_per_change)
                p2_y, p2_remaining = repeats_until(PART_2, max_y, rocks_fallen, y_change, rocks_per_change)
                loop_y = max_y
                use_memory = False
        
        if not use_memory:
            # continue simulation until all remaning rocks fall
            if p1_remaining == 0:
                p1_y += (max_y - loop_y)
            if p2_remaining == 0:
                p2_y += (max_y - loop_y)
            if p1_remaining <= 0 and p2_remaining <= 0:
                return p1_y, p2_y
            p1_remaining -= 1
            p2_remaining -= 1
            
# rocks and move continious generator
rocks = rock_gen()
moves = move_gen()

# terrain setup
terrain = np.zeros((TERRAIN_SPACE, 9), dtype=bool)
terrain[:, 0] = True
terrain[:, -1] = True
terrain[0, :] = True
 
# simulation
p1, p2 = simulate(terrain)
print("Part 1:", p1)
print("Part 2:", p2)