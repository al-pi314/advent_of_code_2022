total = 0
badges = set()
badgesTotal = 0
priority = lambda x: (ord(x.lower()) - ord('a') + 1) + 26 * x.isupper()
for i, line in enumerate(open("input.txt").read().split("\n")):
    items = list(line)
    duplicates = set(items[:len(items) // 2]) & set(items[len(items) // 2:])
    total += sum(map(priority, duplicates))

    if i % 3 == 0:
        badgesTotal += sum(map(priority, badges))
        badges = set(items)
    else:
        badges &= set(items)
badgesTotal += sum(map(priority, badges))

print("Part 1:", total)
print("Part 2:", badgesTotal)