import re

valve_name_idx = {}
valve_tunnels = {}
valve_flowrate = {}
with open("input.txt") as f:
    for line in f:
        matches = re.findall(r".*([A-Z][A-Z]).*=([0-9]+).*valves? ((?: ?[A-Z],?)*)", line)[0]
        valve_name = valve_name_idx.setdefault(matches[0], len(valve_name_idx))
        valve_connections = []
        for tunnel in matches[2].split(","):
            valve_connections.append(valve_name_idx.setdefault(tunnel.strip(), len(valve_name_idx)))

        valve_flowrate[valve_name] = int(matches[1])
        valve_tunnels[valve_name] = valve_connections

def max_water(current, minutes, opened_valves, players, total_time):
    if minutes == 0:
        return 0 if players == 1 else max_water(valve_name_idx["AA"], total_time, opened_valves, players - 1, total_time)

    key = (current, minutes, opened_valves, players)
    if key in memory:
        return memory[key]

    water = 0
    if not (opened_valves & (1 << current)) and valve_flowrate[current] > 0:
        water = max(water, valve_flowrate[current] * (minutes - 1) + max_water(current, minutes -1, opened_valves | (1 << current), players, total_time))
    
    for valve in valve_tunnels[current]:
        water = max(water, max_water(valve, minutes - 1, opened_valves, players, total_time))
    
    memory[key] = water
    return water

memory = {}
print("Part 1:", max_water(valve_name_idx["AA"], 30, 0, 1, 30))
print("Part 2:", max_water(valve_name_idx["AA"], 26, 0, 2, 26))
