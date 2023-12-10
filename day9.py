from itertools import pairwise

def diff1(seq):
    diff = []
    for a, b in pairwise(seq):
        diff.append(b - a)
    return diff

def diffall(seq):
    differences = [seq]
    while True:
        diff = diff1(seq)
        differences.append(diff)
        if all(d == 0 for d in diff):
            break
        seq = diff
    return differences

def extrap(diff_seq):
    new_value = 0
    for i in range(len(diff_seq) - 1, 0, -1):
        diff_seq[i].append(new_value)
        new_value = diff_seq[i-1][-1] + new_value
    return new_value
    
def day9_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    values = [list(map(int, l.split())) for l in lines]
    differences = [diffall(v) for v in values]
    return sum(map(extrap, differences))

def day9_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    values = [list(map(int, reversed(l.split()))) for l in lines]
    differences = [diffall(v) for v in values]
    return sum(map(extrap, differences))

if __name__ == "__main__":
    print("Part 1 example", day9_part1("input/day9_example.txt"))
    print("Part 1", day9_part1("input/day9.txt"))
    print("Part 2 example", day9_part2("input/day9_example.txt"))
    print("Part 2", day9_part2("input/day9.txt"))
