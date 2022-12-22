import re

valve_connections = {}
valve_flow = {}
with open("input.txt") as f:
    for line in f:
        matches = re.findall(r".*([A-Z][A-Z]).*=([0-9]+).*valves? ((?: ?[A-Z],?)*)", line)[0]
        valve_flow[matches[0]] = int(matches[1])
        valve_connections[matches[0]] = list(matches[2].split(", "))

def max_water(current, minutes, flowrate, water, node_flow):
    if minutes == 0:
        return water
    if node_flow.get(current, 0) >= flowrate:
        return water
    node_flow[current] = node_flow.get(current, 0) + valve_flow[current]
    water += valve_flow[current]

    w = 0
    for valve in valve_connections[current]:
        w = max(w, max_water(valve, minutes - 1, flowrate, water, node_flow))
    
        
print("Part 1:", max_water("AA", 30))
