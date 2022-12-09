import numpy as np

moves = {"L": np.array([-1, 0]), "R": np.array([1, 0]), "U": np.array([0, -1]), "D": np.array([0, 1])}
def move_generator():
    with open("input.txt") as f:
        for line in f:
            m1, m2 = line.strip("\n").split(" ")
            for _ in range(int(m2)):
                yield moves[m1]

def knots_positions(n):
    positions = np.zeros((n + 1, 2), dtype=int)
    unique = {(0, 0)}
    for m in move_generator():
        positions[0] += m
        for i in range(1, positions.shape[0]):
            diff = positions[i - 1] - positions[i]
            if max(abs(diff)) <= 1:
                break

            positions[i] += (np.sign(diff) * np.ceil(abs(diff / 2))).astype(int)

            if i == positions.shape[0] -1:
                unique.add(tuple(positions[-1]))
    return len(unique)
    
print("Part 1:", knots_positions(1))
print("Part 2:", knots_positions(9))