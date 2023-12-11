from itertools import combinations

def expand(universe, er, ec):
    h, w = len(universe), len(universe[0])
    eh, ew = h + len(er), w + len(ec)
    expanded = []
    empty_row = "." * ew
    for irow in range(h):
        if irow in er:
            expanded.extend(2*[empty_row])
        else:
            row = list(universe[irow])
            erow = []
            for icol in range(w):
                if icol in ec:
                    erow.extend([".", "."])
                else:
                    erow.append(row[icol])
            expanded.append("".join(erow))
    return expanded
    
def distance(g1, g2):
    return abs(g2[0] - g1[0]) + abs(g2[1] - g1[1])

def distance_expanded(g1, g2, er, ec, factor):
    dr = abs(g2[0] - g1[0])
    dc = abs(g2[1] - g1[1])

    # Expansion factor of two means adding one extra character
    factor -= 1

    # Add factor for each empty row/column in between
    min_row = min(g2[0], g1[0])
    max_row = max(g2[0], g1[0])
    for ir in er:
        if ir > min_row and ir < max_row:
            dr += factor
    
    min_col = min(g2[1], g1[1])
    max_col = max(g2[1], g1[1])
    for ic in ec:
        if ic > min_col and ic < max_col:
            dc += factor
    return dr + dc

def day11_part1(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))
    h, w = len(lines), len(lines[0])

    galaxies = set()
    for il, l in enumerate(lines):
        for ic, c in enumerate(l):
            if c == "#":
                galaxies.add((il, ic))
    
    empty_rows = set(range(h)) - set(g[0] for g in galaxies)
    empty_cols = set(range(w)) - set(g[1] for g in galaxies)
    expanded = expand(lines, empty_rows, empty_cols)

    galaxies = []
    for il, l in enumerate(expanded):
        for ic, c in enumerate(l):
            if c == "#":
                galaxies.append((il, ic))

    dist = 0
    for g1, g2 in combinations(galaxies, 2):
        dist += distance(g1, g2)

    return dist

def day11_part2(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))
    h, w = len(lines), len(lines[0])

    galaxies = set()
    for il, l in enumerate(lines):
        for ic, c in enumerate(l):
            if c == "#":
                galaxies.add((il, ic))
    
    empty_rows = set(range(h)) - set(g[0] for g in galaxies)
    empty_cols = set(range(w)) - set(g[1] for g in galaxies)

    dist = 0
    expansion_factor = int(1e6)
    for g1, g2 in combinations(galaxies, 2):
        dist += distance_expanded(g1, g2, empty_rows, empty_cols, expansion_factor)
    
    return dist

if __name__ == "__main__":
    print("Part 1 example", day11_part1("input/day11_example.txt"))
    print("Part 1", day11_part1("input/day11.txt"))
    print("Part 2 example", day11_part2("input/day11_example.txt"))
    print("Part 2", day11_part2("input/day11.txt"))
