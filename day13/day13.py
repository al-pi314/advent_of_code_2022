from functools import cmp_to_key


def read_list(line, i):
    if i >= len(line):
        raise SyntaxError("no matching ]")
    if line[i] == "]":
        return [], i
    result = []
    element = 0
    while True:
        if line[i] == "[":
            sub_list, i = read_list(line, i + 1)
            element = sub_list
        elif line[i] == "]":
            result.append(element)
            return result, i
        elif line[i] == ",":
            result.append(element)
            element = 0
        else:
            element *= 10
            element += int(line[i])
        i += 1

def read_list_from_line(line):
    l, _ = read_list(line, 1)
    return l
    
def packet_reader():
    with open('input.txt') as f:
        while True:
            p1 = read_list_from_line(f.readline())
            p2 = read_list_from_line(f.readline())
            yield p1, p2
            if f.readline() == "":
                break

def are_sorted(packet1, packet2):
    packet1_is_int = isinstance(packet1, int)
    packet2_is_int = isinstance(packet2, int)
    
    if packet1_is_int and packet2_is_int:
        return packet1 < packet2, packet1 > packet2
    elif packet1_is_int:
        packet1 = [packet1]
    elif packet2_is_int:
        packet2 = [packet2]
    
    longest = max(len(packet1), len(packet2))
    for i in range(longest):
        if i >= len(packet1):
            return True, False
        if i >= len(packet2):
            return False, True
        increasing, decreasing = are_sorted(packet1[i], packet2[i])
        if increasing or decreasing:
            return increasing, decreasing
    return True, False

result = 0
packets = []
for i, (p1, p2) in enumerate(packet_reader(), start=1):
    increasing, decreasing = are_sorted(p1, p2)
    if increasing:
        result += i
    packets.extend([p1, p2])
print("Part 1:", result)

decoders = [[[2]], [[6]]]
packets.extend(decoders)
def comparator(p1, p2):
    increasing, decreasing = are_sorted(p1, p2)
    if increasing:
        return -1
    elif decreasing:
        return 1
    else:
        return 0
packets.sort(key=cmp_to_key(comparator))
result = 1
for decoder in decoders:
    result *= (packets.index(decoder) + 1)
print("Part 2:", result)