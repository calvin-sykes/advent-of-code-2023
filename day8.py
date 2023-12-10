from itertools import cycle
from math import lcm

def day8_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    path = [0 if c == "L" else 1 for c in lines[0][:-1]]

    nodes = {}
    for l in lines[1:]:
        try:
            node, dirs = l.split("=")
            left, right = map(lambda s: s.strip("() \n"), dirs.split(","))
            nodes[node.strip()] = (left, right)
        except:
            continue

    num_steps = 0
    current_node = "AAA"
    for direction in cycle(path):
        #old_node = current_node
        current_node = nodes[current_node][direction]
        num_steps += 1
        #print(f"turned {'R' if direction else 'L'} from {old_node} to reach {current_node}")
        if current_node == "ZZZ":
            break

    return num_steps

def day8_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    path = [0 if c == "L" else 1 for c in lines[0][:-1]]

    nodes = {}
    for l in lines[1:]:
        try:
            node, dirs = l.split("=")
            left, right = map(lambda s: s.strip("() \n"), dirs.split(","))
            nodes[node.strip()] = (left, right)
        except:
            continue

    start_nodes = list(filter(lambda s: s.endswith("A"), nodes.keys()))
    end_nodes = set(filter(lambda s: s.endswith("Z"), nodes.keys()))

    num_steps = 0
    current_nodes = start_nodes.copy()

    cycle_lengths = []
    for start_node in start_nodes:
        num_steps = 0
        current_node = start_node
        for direction in cycle(path):
            current_node = nodes[current_node][direction]
            num_steps += 1
            if current_node in end_nodes:
                break
        cycle_lengths.append(num_steps)
    return lcm(*cycle_lengths)

if __name__ == "__main__":
    print("Part 1 example", day8_part1("input/day8_example.txt"))
    print("Part 1", day8_part1("input/day8.txt"))
    print("Part 2 example", day8_part2("input/day8_example_part2.txt"))
    print("Part 2", day8_part2("input/day8.txt"))
