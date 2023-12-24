from collections import defaultdict, deque

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def get_neighbours(grid, r, c, h, w, ignore_direction):
    neighbours = []
    for nd, (dr, dc) in zip(range(4), D.shifts):
        nr = r + dr
        nc = c + dc
        if nr == -1 or nr == h or nc == -1 or nc == w:
            continue # OOB
        if grid[nr][nc] == "#":
            continue # wall
        if not ignore_direction and grid[nr][nc] in "^>v<":
            slope_dirn = "^>v<".index(grid[nr][nc])
            if slope_dirn != nd:
                continue # Wrong slope direction
        neighbours.append((nd, (nr, nc)))
    return neighbours

def find_longest_path(grid, ignore_direction):
    h, w = len(grid), len(grid[0])

    sr = 0
    sc = grid[sr].index(".")
    
    er = h - 1
    ec = grid[er].index(".")
    
    nodes = []
    for r in range(h):
        for c in range(w):
            if grid[r][c] == "#":
                continue
            ngb = get_neighbours(grid, r, c, h, w, True)
            if len(ngb) > 2:
                nodes.append((r, c))

    ordA = ord("A")
    node_names = []
    for i in range(len(nodes)):
        if i < 26:
            node_names.append(chr(ordA + i))
        else:
            node_names.append(chr(ordA + i // 26) + chr(ordA + i % 26))
    nodes = [(sr, sc)] + nodes + [(er, ec)]
    node_names = ["s"] + node_names + ["e"]

    edges = defaultdict(dict)
    for i, (nr, nc) in enumerate(nodes[:-1]):
        name = node_names[i]
        seen = {(nr, nc)}
        neighbours = get_neighbours(grid, nr, nc, h, w, ignore_direction)
        for dirn, ngb in neighbours:
            r, c = ngb
            l = 0
            while True:
                seen.add((r, c))
                l += 1
                if (r, c) in nodes: # edge found
                    name_other = node_names[nodes.index((r, c))]
                    edges[name][name_other] = l
                    break
                found = False
                for dirn, ngb in get_neighbours(grid, r, c, h, w, ignore_direction):
                    if ngb not in seen:
                        r, c = ngb
                        found = True
                if not found:
                    break

    stack = deque()
    stack.append(("s", ["s"]))
    longest_path = [[], 0]
    while stack:
        n, path = stack.pop()
        if n == "e":
            l = sum(edges[path[i]][path[i+1]] for i in range(len(path)-1))
            if l > longest_path[1]:
                longest_path = [path, l]
        for e in edges[n]:
            if e not in path:
                stack.append((e, path + [e]))

    return longest_path

def day23_part1(filename):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())
        grid = [list(l) for l in lines]

    _, length = find_longest_path(grid, False)
    print(_)
    return length

def day23_part2(filename):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())
        grid = [list(l) for l in lines]

    _, length = find_longest_path(grid, True)
    print(_)
    return length

if __name__ == "__main__":    
    print("Part 1 example", day23_part1("input/day23_example.txt"))
    print("Part 1", day23_part1("input/day23.txt"))
    print("Part 2 example", day23_part2("input/day23_example.txt"))
    print("Part 2", day23_part2("input/day23.txt"))
