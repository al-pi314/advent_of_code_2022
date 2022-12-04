
def sections(line):
    s = line.split(",")
    return list(map(int, [*s[0].split("-"), *s[1].split("-")]))

def includes(a, c, d, b):
    return a <= c and d <= b

def overlaps(a, c, d, b):
    return c <= a <= d or c <= b <= d

def is_valid(a, b, c, d, f=includes):
    return f(a, c, d, b) or f(c, a, b, d)

# fnc = includes # Part 1
# fnc = overlaps # Part 2
fnc = overlaps
total = 0
for line in open("input.txt").read().split("\n"):
    a, b, c, d = sections(line)
    if is_valid(a, b, c, d, f=fnc):
        total += 1
print(total)