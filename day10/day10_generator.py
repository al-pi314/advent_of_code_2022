def command_generator():
    with open("input.txt") as f:
        for line in f:
            yield None
            if line.startswith("addx"):
                yield int(line.split(" ")[1])
# Part 1
interesting_cycle = (x for x in [20, 60, 100, 140, 180, 220])
intr_cylce = next(interesting_cycle)
signal_strength = 0

# Part 2
display = [["." for _ in range(40)] for _ in range(6)]

X = 1
for cycle, cmd in enumerate(command_generator()):
    # Part 2 (current cycle start)
    display[int(cycle / 40)][cycle % 40] = "." if abs(cycle % 40 - X) > 1 else "#"
    
    # Part 1 (previous cycle end)
    cycle += 1
    if cycle == intr_cylce:
        signal_strength += cycle * X
        intr_cylce = next(interesting_cycle, -1)

    # (current cycle middle)
    if cmd is not None:
        X += cmd    

print("Part 1:", signal_strength)
print("Part 2:")
for row in display:
    print(" ".join(row))