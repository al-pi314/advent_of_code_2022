# Part 1
interesting_cycles = [20, 60, 100, 140, 180, 220]
idx = 0
interesting_signal_strength = 0

# Part 2
display = [[]]
def draw(sprite_pos):
    global display
    if len(display[-1]) == 40:
        display.append([])
    if abs(len(display[-1]) - sprite_pos) <= 1:
        display[-1].append("#")
    else:
        display[-1].append(".")

with open("input.txt") as f:
    cycle = 1
    X_prev = 1
    X = 1
    for line in f:
        draw(X)
        if idx < len(interesting_cycles) and cycle >= interesting_cycles[idx]:
            register_val = X if cycle == interesting_cycles[idx] else X_prev
            interesting_signal_strength += interesting_cycles[idx] * register_val
            idx += 1
        
        if line.startswith("noop"):
            cycle += 1
            continue
        
        X_prev = X
        X += int(line.split(" ")[1])
        cycle += 2
        draw(X_prev)

print("Part 1:", interesting_signal_strength)
print("Part 2:")
for row in display:
    print(" ".join(row))