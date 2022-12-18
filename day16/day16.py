import re
from functools import lru_cache


def read_valves():
    valve_connections = {}
    valve_flow = {}
    with open("input.txt") as f:
        for line in f:
            matches = re.findall(r".*([A-Z][A-Z]).*=([0-9]+).*valves? ((?: ?[A-Z],?)*)", line)[0]
            valve_flow[matches[0]] = int(matches[1])
            valve_connections[matches[0]] = list(matches[2].split(", "))
    return valve_connections, valve_flow

def lru_wrapper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
    
@lru_wrapper
@lru_cache
def release_flow(opened_valves, current_valve, total_flow, minutes):
    if minutes == 0:
        return total_flow
    
    released_flow = total_flow
    if current_valve  not in opened_valves and valve_flow[current_valve] > 0:
        opened_valves.add(current_valve)
        released_flow = max(released_flow, release_flow(opened_valves, current_valve, total_flow + valve_flow[current_valve] * (minutes -1), minutes - 1))
        opened_valves.remove(current_valve)
    
    for valve in valve_connections[current_valve]:
        move_released_flow = release_flow(opened_valves, valve, total_flow, minutes - 1)
        released_flow = max(released_flow, move_released_flow)
    
    return released_flow

valve_connections, valve_flow = read_valves()
print(release_flow(set(), "AA", 0, 30))