from itertools import chain
from tqdm import trange

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    s = {NORTH: "N", EAST: "E", SOUTH: "S", WEST: "W"}

def to_string(pattern):
    return "\n".join("".join(l) for l in pattern)
        
def transpose(pattern):
    # Make columns of pattern
    transposed = [list() for _ in range(len(pattern[0]))]
    for l in pattern:
        for i, c in enumerate(l):
            transposed[i].append(c)
    return transposed
    
def slide(pattern, reverse=False):
    if reverse:
        pattern = [l[::-1] for l in pattern]
    
    slid_pattern = []
    for col in pattern:
        slid_col = []
        # if ., continue
        # if #, mark position
        # if O, move forward to last_cube
        last_cube = -1
        for i, c in enumerate(col):
            if c == ".":
                slid_col.append(c)
            elif c == "#":
                slid_col.append(c)
                last_cube = i
            elif c == "O":
                slid_col.insert(last_cube+1, c)
                last_cube += 1
        slid_pattern.append(slid_col)

    if reverse:
        slid_pattern = [l[::-1] for l in slid_pattern]
    return slid_pattern

def tilt(pattern, direction):
    if direction in (D.NORTH, D.SOUTH):
        pattern = transpose(pattern)

    reverse = direction in (D.SOUTH, D.EAST)
    tilted = slide(pattern, reverse)

    if direction in (D.NORTH, D.SOUTH):
        return transpose(tilted)
    else:
        return tilted

def spin_cycle(pattern):
    for dirn in (D.NORTH, D.WEST, D.SOUTH, D.EAST):
        pattern = tilt(pattern, dirn)
    return pattern

def load(pattern):
    load = 0
    for i, l in enumerate(pattern):
        load_factor = len(pattern) - i
        load += load_factor * sum(c == "O" for c in l)
    return load

def day14_part1(filename):
    with open(filename) as f:
        lines = f.readlines()
        lines = [l.rstrip("\n") for l in lines] # remove newlines

    tilted = tilt(lines, D.NORTH)
    return load(tilted)

def day14_part2(filename):
    with open(filename) as f:
        lines = f.readlines()
        lines = [l.rstrip("\n") for l in lines] # remove newlines

    it = 0
    spun = lines
    cache = {}
    cycle_length = -1
    cycle_start = -1
    N = 1000000000
    while True:
        spun = spin_cycle(spun)
        it += 1
        
        if cycle_length == -1:
            pstr = to_string(spun)
            if pstr in cache:
                cycle_start = it
                cycle_length = it - cache[pstr]
                break
            else:
                cache[pstr] = it
    
    reverse_cache = {v: k for k, v in cache.items()}
    offset = cycle_start - cycle_length
    index = (N - offset) % cycle_length + offset
    return load(reverse_cache[index].split("\n"))

if __name__ == "__main__":
    print("Part 1 example", day14_part1("input/day14_example.txt"))
    print("Part 1", day14_part1("input/day14.txt"))
    print("Part 2 example", day14_part2("input/day14_example.txt"))
    print("Part 2", day14_part2("input/day14.txt"))
