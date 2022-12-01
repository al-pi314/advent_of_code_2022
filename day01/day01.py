# Part 1 --> k = 1
# Part 2 --> k = 3
k = 3
print(sum(list(sorted([sum(int(item) for item in inventory.split("\n")) for inventory in open("./input.txt").read().split("\n\n")]))[-3:]))

# from functools import reduce

# k=3
# print(sum( reduce(lambda l, x: list(sorted(l + [x]))[-k:], 
#     [sum(map(int, inventory.splitlines())) for inventory in open("./input.txt").read().split("\n\n")]
# ,[])))

# from functools import reduce

# k=3
# print(sum(
#     reduce(
#         lambda l, x: (l[0],  l[1] + int(x)) if x != "\n" else (list(sorted(l[0] + [l[1]]))[-k:], 0), 
#         open("./input.txt").readlines(), 
#         ([],0)
#     )[0]
# ))

