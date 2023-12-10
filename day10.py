from itertools import cycle

class D:
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    s = {UP: "UP", RIGHT: "RIGHT", DOWN: "DOWN", LEFT: "LEFT"}

def prettyprint(field_str):
    transtable = str.maketrans("|-LJ7F", "\u2502\u2500\u2514\u2518\u2510\u250c")
    box_str = field_str.translate(transtable)
    print(box_str)

def new_dir(c, curr_dir):
    match c:
        case "|" | "-":
            return curr_dir
        case "L":
            return D.RIGHT if curr_dir == D.DOWN else D.UP
        case "J":
            return D.LEFT if curr_dir == D.DOWN else D.UP
        case "7":
            return D.LEFT if curr_dir == D.UP else D.DOWN
        case "F":
            return D.RIGHT if curr_dir == D.UP else D.DOWN
        case _:
            raise ValueError(f"Invalid character {c}")

def shift(dirn):
    match dirn:
        case D.UP:
            return (-1, 0)
        case D.RIGHT:
            return (0, 1)
        case D.DOWN:
            return (1, 0)
        case D.LEFT:
            return (0, -1)
        case _:
            raise ValueError(f"Invalid direction {dirn}")

def find_loop(lines):
    # Find start
    ij = None
    for il, l in enumerate(lines):
        if "S" in l:
            ij = l.index("S")
            break
    if ij is None:
        raise ValueError("No start in loop")

    # Find initial direction
    if lines[il-1][ij] in "|F7":
        direction = D.UP
    elif lines[il][ij+1] in "-J7":
        direction = D.RIGHT
    elif lines[il+1][ij] in "|LJ":
        direction = D.DOWN
    elif lines[il][ij-1] in "-LF":
        direction = D.LEFT
    else:
        raise ValueError

    coords = [(il, ij)]
    dirs = [direction]
    
    dl, dj = shift(direction)
    il += dl
    ij += dj
    c = lines[il][ij]
    while c != "S":
        direction = new_dir(c, direction)
        coords.append((il, ij))
        dirs.append(direction)
        dl, dj = shift(direction)
        il += dl
        ij += dj
        c = lines[il][ij]
    return coords, dirs
        
def day10_part1(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))

    coords, _ = find_loop(lines)
    return len(coords) // 2

def day10_part2(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))

    h, w = len(lines), len(lines[0])
    coords, dirs = find_loop(lines)

    # Double the field in size, filling gaps with blanks
    lines2 = []
    for il in range(h*2):
        if il % 2 == 0:
            lines2.append(list(",".join(lines[il//2])))
        else:
            lines2.append(list(s for (s,_) in zip(cycle(" ,"), range(w*2))))
    h, w = len(lines2), len(lines2[0])

    # Add extra pipes to reconnect the loop
    coords2 = []
    for ic in range(len(coords)):
        il, ij = map(lambda c: c * 2, coords[ic])
        dirn = dirs[ic]
        dl, dj = shift(dirn)
        coords2.extend([(il, ij), (il+dl, ij+dj)])
        lines2[il+dl][ij+dj] = "|" if dirn in (D.UP, D.DOWN) else "-"
    coords_set = set(coords2)

    # Find tiles possibly enclosed by the loop
    maybe_inside = set()
    for il in range(h):
        for ij in range(w):
            # Skip if part of loop
            if (il, ij) in coords_set:
                continue
            # Outside if on boundary
            elif il == 0 or il == h-1 or ij == 0 or ij == w-1:
                lines2[il][ij] = "O"
            else:
                maybe_inside.add((il, ij))
                lines2[il][ij] = "?"

    # Loop over maybe_inside, test for adjacency to outside, and remove if so
    # Repeat until no tiles changed in a pass
    shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    while True:
        removed = set()
        for (il, ij) in maybe_inside:
            outside = False
            # Check for immediately adjacent outside tiles
            for dl, dj in shifts:
                if lines2[il+dl][ij+dj] is "O":
                    lines2[il][ij] = "O"
                    removed.add((il, ij))
                    break
        if len(removed) == 0:
            break
        else:
            maybe_inside -= removed
    
    # All remaining tiles are inside
    for (il, ij) in maybe_inside:
        lines2[il][ij] = "I"
    
    result = "\n".join("".join(l[::2]) for l in lines2[::2])
    #print("After compressing back to original field size")
    #prettyprint(result)

    return result.count("I")

if __name__ == "__main__":
    print("Part 1 example", day10_part1("input/day10_example.txt"))
    print("Part 1 second example", day10_part1("input/day10_example2.txt"))
    print("Part 1", day10_part1("input/day10.txt"))
    print("Part 2 example", day10_part2("input/day10_part2_example1.txt"))
    print("Part 2 second example", day10_part2("input/day10_part2_example2.txt"))
    print("Part 2 third example", day10_part2("input/day10_part2_example3.txt"))
    print("Part 2 fourth example", day10_part2("input/day10_part2_example4.txt"))
    print("Part 2", day10_part2("input/day10.txt"))
