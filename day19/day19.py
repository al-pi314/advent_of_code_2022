import numpy as np

blueprints = [
    np.array([4, 0, 0, 0]),
    np.array([2, 0, 0, 0]),
    np.array([3, 14, 0, 0]),
    np.array([2, 0, 7, 0])
]


def build_robots(robots, resources, robot_type=0):
    if robot_type > 3:
        return []
    
    options = build_robots(robots, resources, robot_type +1)
    if (blueprints[robot_type] <= resources).all():
        n_robots = robots.copy()
        n_robots[robot_type] += 1
        n_resources = resources - blueprints[robot_type]

        options.append((n_robots, n_resources))
        options += build_robots(n_robots, n_resources, robot_type)
    return options

def tick(robots, resources, minutes):
    # no geodes collected
    if minutes <= 0:
        return robots[3]

    # construct all possible build plans
    build_plans = [(robots, resources)] + build_robots(robots, resources)

    # compare different build plans
    geodes = 0
    for (new_robots, remaining_resources) in build_plans:
        geodes = max(geodes, tick(new_robots, remaining_resources + robots, minutes - 1))
    return geodes
 
print(tick(np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0]), 19))