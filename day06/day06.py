buffer = open("input.txt", "r").readline()

def find_marker(buffer, marker_len):
    marker = [None for _ in range(marker_len)]
    for i, char in enumerate(buffer):
        marker[i % len(marker)] = char
        if i < len(marker):
            continue
        if len(set(marker)) == marker_len:
            return i + 1

print("Part 1:", find_marker(buffer, 4))
print("Part 2:", find_marker(buffer, 14))