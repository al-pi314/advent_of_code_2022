import numpy as np

moves = {"L": np.array([-1, 0]), "R": np.array([1, 0]), "U": np.array([0, -1]), "D": np.array([0, 1])}
def move_generator():
    with open("input.txt") as f:
        for line in f:
            m1, m2 = line.strip("\n").split(" ")
            for _ in range(int(m2)):
                yield moves[m1]
# <3 this 

# # ce bi delu z rekurzijo:
# def premakni(knots):
#     l, _ = knots.shape
#     diff = knots[1] - knots[0]
#     if max(abs(diff)) <= 1:
#         return
#     knots[1] += np.sign(diff)
#     if l == 2:
#         unique.add(tuple(knots[-1]))
#     else:
#         premakni(knots[1:])

def knots_positions(n):
    positions = np.zeros((n + 1, 2), dtype=int)
    unique = {(0, 0)}
    for m in move_generator():
        positions[0] += m
        for i in range(1, positions.shape[0]):
            diff = positions[i - 1] - positions[i]
            if max(abs(diff)) <= 1:
                break
            
            # positions[i] += (np.sign(diff) * np.ceil(abs(diff / 2))).astype(int)
            # abs diff je lahko : 0,2  2,0  1,2  2,1
            # after ceil(x/ 2) je lahko : 0,1  1,0  1,1  1,1 kr je isto kot abs sign
            # (abs sign) * sign == sign
            positions[i] += np.sign(diff)

            if i == positions.shape[0] -1:
                unique.add(tuple(positions[-1]))
    return len(unique)

print("Part 1:", knots_positions(1))
print("Part 2:", knots_positions(9))