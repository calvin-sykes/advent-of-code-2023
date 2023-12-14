class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def to_string(pattern):
    return "\n".join("".join(l) for l in pattern)
        
def transpose(pattern):
    transposed = [list() for _ in range(len(pattern[0]))]
    for l in pattern:
        for i, c in enumerate(l):
            transposed[i].append(c)
    return transposed
    
def slide(pattern, reverse=False):
    if reverse:
        pattern = [l[::-1] for l in pattern]
    
    slid_pattern = []
    for l in pattern:
        slid = []
        # if ., continue
        # if #, mark position
        # if O, move forward to last_cube
        last_cube = -1
        for i, c in enumerate(l):
            if c == ".":
                slid.append(c)
            elif c == "#":
                slid.append(c)
                last_cube = i
            elif c == "O":
                slid.insert(last_cube + 1, c)
                last_cube += 1
        slid_pattern.append(slid)

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
        pattern = [l.rstrip("\n") for l in f.readlines()] # remove newlines

    tilted = tilt(pattern, D.NORTH)
    return load(tilted)

def day14_part2(filename):
    with open(filename) as f:
        pattern = [l.rstrip("\n") for l in f.readlines()] # remove newlines

    it = 0
    cache = {}
    cycle_length = None
    while True:
        pattern = spin_cycle(pattern)
        if not cycle_length:
            pstr = to_string(pattern)
            if pstr in cache:
                cycle_start = it
                cycle_length = it - cache[pstr]
                break
            else:
                cache[pstr] = it
        it += 1

    N = 1000000000
    offset = cycle_start - cycle_length
    index = (N - 1 - offset) % cycle_length + offset
    for pstr, it in cache.items():
        if it == index:
            return load(pstr.split("\n"))

if __name__ == "__main__":
    print("Part 1 example", day14_part1("input/day14_example.txt"))
    print("Part 1", day14_part1("input/day14.txt"))
    print("Part 2 example", day14_part2("input/day14_example.txt"))
    print("Part 2", day14_part2("input/day14.txt"))
