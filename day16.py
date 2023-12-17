from collections import defaultdict
from itertools import product
from tqdm import tqdm

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def beam(grid, rs, cs, d, energised=None):
    h, w = len(grid), len(grid[0])
    dr, dc = D.shifts[d]
    r, c = rs + dr, cs + dc

    if energised is None:
        energised = defaultdict(int)
    
    while True:
        if r < 0 or r == h or c < 0 or c == w:
            break
        i = r * w + c
        dd = 1 << d
        if energised[i] & dd:
            break
        else:
            energised[i] |= dd
        match grid[r][c]:
            case "/":  d ^= 0b01
            case "\\": d ^= 0b11
            case "|" if (d & 1):
                beam(grid, r, c, D.NORTH, energised)
                beam(grid, r, c, D.SOUTH, energised)
                break
            case "-" if not d & 1:
                beam(grid, r, c, D.EAST, energised)
                beam(grid, r, c, D.WEST, energised)
                break
        dr, dc = D.shifts[d]
        r += dr
        c += dc
    return energised

def day16_part1(filename):
    with open(filename) as f:
        grid = f.read().rstrip("\n").split("\n")
    h, w = len(grid), len(grid[0])
    
    energised = beam(grid, 0, -1, D.EAST)
    return len(energised)

def day16_part2(filename):
    with open(filename) as f:
        grid = f.read().rstrip("\n").split("\n")
    h, w = len(grid), len(grid[0])
    
    start_positions = \
        [( n,  h, D.NORTH) for n in range(w)] + \
        [( n, -1, D.EAST ) for n in range(h)] + \
        [(-1,  n, D.SOUTH) for n in range(w)] + \
        [( n,  w, D.WEST ) for n in range(h)]

    max_energised = 0
    for start in start_positions:
        energised = beam(grid, *start)
        max_energised = max(max_energised, len(energised))
    
    return max_energised

if __name__ == "__main__":
    print("Part 1 example", day16_part1("input/day16_example.txt"))
    print("Part 1", day16_part1("input/day16.txt"))
    print("Part 2 example", day16_part2("input/day16_example.txt"))
    print("Part 2", day16_part2("input/day16.txt"))
