import re

from intervals import Interval


def sensor_reading_generator():
    with open("input.txt") as f:
        for line in f:
            result = re.findall(r"[a-zA-Z]*=(-?[0-9]*)", line)
            yield tuple(int(x) for x in result)

def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

limit = 4000000
interest_y = 2000000

y_intervals = [Interval(-1,-1) for _ in range(limit + 1)]
full_coverage = set()
for i, sensor_reading in enumerate(sensor_reading_generator()):
    to_beacon = distance(*sensor_reading)
    y_lower = max(sensor_reading[1] - to_beacon, 0)
    y_upper = min(sensor_reading[1] + to_beacon, limit)
    for y in range(y_lower, y_upper + 1):
        if y in full_coverage:
            continue

        distance_to_y = distance(sensor_reading[0], y, sensor_reading[0], sensor_reading[1])
        coverage_distance_at_y = (2 * to_beacon + 1) - 2 * distance_to_y
        if coverage_distance_at_y <= 0:
            continue

        coverage_interval = (sensor_reading[0] - coverage_distance_at_y // 2, sensor_reading[0] + coverage_distance_at_y // 2)
        if y != interest_y:
            coverage_interval = (max(coverage_interval[0], 0), min(coverage_interval[1], limit))
        y_intervals[y] = y_intervals[y].insert(Interval(*coverage_interval))

        if y_intervals[y].total_length() == limit + 1:
            full_coverage.add(y)
    print(f"... finished {i} sensor readings ...")

print("Part 1:", y_intervals[interest_y].total_length())
for y in range(limit + 1):
    if y in full_coverage:
        continue
    x = y_intervals[y].non_covered_x(limit)
    if x is not None:
        print("Part 2:", y + x * limit)