# buffer = open("input.txt", "r").readline()

# def find_marker(buffer, marker_len):
#     for i in range(marker_len, len(buffer) + 1):
#         if len(set(buffer[i - marker_len:i])) == marker_len:
#             return i

# print("Part 1:", find_marker(buffer, 4))
# print("Part 2:", find_marker(buffer, 14))

buffer = open("input.txt", "r").readline()
print("Part 1:", next(i for i in range(4, len(buffer) + 1) if len(set(buffer[i - 4:i])) == 4))
print("Part 2:", next(i for i in range(14, len(buffer) + 1) if len(set(buffer[i - 14:i])) == 14))