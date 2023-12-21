from itertools import pairwise

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]

dirn_map = {c : d for c, d in zip("URDL", range(4))}

def day18_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    instructions = []
    colours = []

    for l in lines:
        dirn, length, _ = l.split()
        instructions.append((dirn, int(length)))

    coords = [(0, 0)]
    for i in instructions:
        y, x = coords[-1]
        dirn = dirn_map[i[0]]
        dy, dx = D.shifts[dirn]
        coords.append((y + dy * i[1], x + dx * i[1]))
    assert coords[-1] == (0, 0)

    miny = min(coords, key=lambda c: c[0])[0]
    minx = min(coords, key=lambda c: c[1])[1]
    maxy = max(coords, key=lambda c: c[0])[0]
    maxx = max(coords, key=lambda c: c[1])[1]

    yshift = xshift = 0
    if miny < 0:
        yshift = -miny
        maxy += yshift
    if minx < 0:
        xshift = -minx
        maxx += xshift        

    grid = [["." for _ in range(maxx+1)] for __ in range(maxy+1)]

    dug_count = 0
    
    for (y1, x1), (y2, x2) in pairwise(coords):
        if x1 != x2:
            if x2 < x1:
                x1, x2 = x2, x1
            for ix in range(x1, x2+1):
                grid[y1+yshift][ix+xshift] = "#"
            dug_count += x2 - x1
        elif y1 != y2:
            if y2 < y1:
                y1, y2 = y2, y1
            for iy in range(y1, y2+1):
                grid[iy+yshift][x1+xshift] = "#"
            dug_count += y2 - y1
        else:
            raise ValueError
        
    for y, l in enumerate(grid):
        x = 0
        parity = 0
        while x < maxx:
            c = l[x]
            if c == "#":
                if l[x+1] == "#":
                    xs = x
                    while x < maxx and l[x+1] == "#":
                        x += 1
                    xe = x
                    if y < maxy and grid[y+1][xs] == "#":
                        dir_start = D.SOUTH
                    elif y > 0 and grid[y-1][xs] == "#":
                        dir_start = D.NORTH
                    if y < maxy and grid[y+1][xe] == "#":
                        dir_end = D.SOUTH
                    elif y > 0 and grid[y-1][xe] == "#":
                        dir_end = D.NORTH                
                    if dir_start == dir_end:
                        x += 1
                        continue
                parity ^= 1
            else:
                if parity and grid[y][x] == ".":
                    grid[y][x] = "o"
                    dug_count += 1
            x += 1
    
    return dug_count

    
def day18_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    instructions = []
    colours = []

    for l in lines:
        *_, colour = l.split()
        length = int(colour[2:7], base=16)
        dirn = "RDLU"[int(colour[7])]
        instructions.append((dirn, length))

    coords = [(0, 0)]
    for i in instructions:
        y, x = coords[-1]
        dirn = dirn_map[i[0]]
        dy, dx = D.shifts[dirn]
        coords.append((y + dy * i[1], x + dx * i[1]))
    assert coords[-1] == (0, 0)

    miny = min(coords, key=lambda c: c[0])[0]
    minx = min(coords, key=lambda c: c[1])[1]
    maxy = max(coords, key=lambda c: c[0])[0]
    maxx = max(coords, key=lambda c: c[1])[1]

    area = 0
    peri = 0
    for (y1, x1), (y2, x2) in pairwise(coords):
        area += (x2 + x1) * (y2 - y1)
        peri += abs(x2 - x1) + abs(y2 - y1)
    area //= 2
    cubearea = area + peri // 2 + 1
    return cubearea

if __name__ == "__main__":
    print("Part 1 example", day18_part1("input/day18_example.txt"))
    print("Part 1", day18_part1("input/day18.txt"))
    print("Part 2 example", day18_part2("input/day18_example.txt"))
    print("Part 2", day18_part2("input/day18.txt"))
