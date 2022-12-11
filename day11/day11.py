from heapq import nlargest


def get_function(operator, right_operand):
    operation_base = lambda a, b: a + b
    if operator == "*":
        operation_base = lambda a, b: a * b
    
    if right_operand == "old":
        return lambda old: operation_base(old, old)

    return lambda old: operation_base(old, int(right_operand))

def read_monkey_logic(f):
    f.readline() # discard
    items = list(map(int, f.readline().split(": ")[1].split(", ")))
    operator, value = f.readline().strip("\n").split("d ")[1].split(" ")
    operation = get_function(operator, value)
    divisor = int(f.readline().split("y ")[1])
    if_true = int(f.readline().split("y ")[1])
    if_false = int(f.readline().split("y ")[1])
    f.readline() # discard
    return items, operation, divisor, if_true, if_false

monkeys = 8
inspections = [0 for _ in range(monkeys)]
global_divisor = 1

monkey_items = []
monkey_operations = []
monkey_divisors = []
monkey_if_true = []
monkey_if_false = []
with open("input.txt") as f:
    for _ in range(monkeys):
        items, operation, divisor, if_true, if_false = read_monkey_logic(f)
        global_divisor *= divisor

        monkey_items.append(items)
        monkey_operations.append(operation)
        monkey_divisors.append(divisor)
        monkey_if_true.append(if_true)
        monkey_if_false.append(if_false)

def get_monkey_bussiness(rounds, relief, use_global_divisor=False):
    for _ in range(rounds):
        for i in range(monkeys):
            inspections[i] += len(monkey_items[i])
            for item in monkey_items[i]:
                value = int(monkey_operations[i](item) / relief)
                if use_global_divisor:
                    value %= global_divisor
                if value % monkey_divisors[i] == 0:
                    monkey_items[monkey_if_true[i]].append(value)
                else:
                    monkey_items[monkey_if_false[i]].append(value)
            monkey_items[i] = []
    first, second = nlargest(2, inspections)
    return first * second

# Only one of the following two lines should be uncommented
# print("Part 1:", get_monkey_bussiness(20, 3, use_global_divisor=False))
print("Part 2:", get_monkey_bussiness(10000, 1, use_global_divisor=True))