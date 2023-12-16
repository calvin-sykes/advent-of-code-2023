from collections import defaultdict

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

def nudge(r, c, d):
    shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dr, dc = shifts[d]
    return r + dr, c + dc

def beam(grid, rs, cs, d, energised=None):
    h, w = len(grid), len(grid[0])
    r, c = nudge(rs, cs, d)

    if energised is None:
        energised = defaultdict(int)
    
    while True:
        if r < 0 or r > h - 1 or c < 0 or c > w - 1:
            break
        if (r, c) in energised and energised[(r, c)] & (1 << d):
            break
        else:
            energised[r, c] |= 1 << d
        square = grid[r][c]
        match square:
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
        r, c = nudge(r, c, d)
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
    for rs, cs, d in start_positions:
        energised = beam(grid, rs, cs, d)
        max_energised = max(max_energised, len(energised))
    
    return max_energised

if __name__ == "__main__":
    print("Part 1 example", day16_part1("input/day16_example.txt"))
    print("Part 1", day16_part1("input/day16.txt"))
    print("Part 2 example", day16_part2("input/day16_example.txt"))
    print("Part 2", day16_part2("input/day16.txt"))
