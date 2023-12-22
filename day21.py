from collections import deque, defaultdict

def get_neighbours(grid, h, w, r, c):
    neighbours = []
    for dr, dc in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
        nr = r + dr
        nc = c + dc
        if nr == -1 or nr == h or nc == -1 or nc == w:
            continue # OOB
        elif grid[nr][nc] == "." or grid[nr][nc] == "S":
            neighbours.append((nr, nc))
    return neighbours

def get_neighbours_pbc(grid, h, w, r, c):
    neighbours = []
    for dr, dc in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
        nr = (r + dr) % h
        nc = (c + dc) % w
        if grid[nr][nc] == "." or grid[nr][nc] == "S":
            neighbours.append((r+dr, c+dc))
    return neighbours

def day21_part1(filename, nsteps):
    with open(filename) as f:
        grid = list(map(lambda s: list(s.rstrip("\n")), f.readlines()))
    h, w = len(grid), len(grid[0])

    for sy, l in enumerate(grid):
        if "S" in l:
            sx = l.index("S")
            break

    starts = {(sy, sx)}
    for i in range(nsteps):
        newstarts = set()
        for start_tile in starts:
            for ngb in get_neighbours(grid, h, w, *start_tile):
                newstarts.add(ngb)
        starts = newstarts
        
    return len(starts)

def day21_part2(filename, n_steps):
    with open(filename) as f:
        grid = list(map(lambda s: list(s.rstrip("\n")), f.readlines()))
    h, w = len(grid), len(grid[0])
    assert h == w

    for sy, l in enumerate(grid):
        if "S" in l:
            sx = l.index("S")
            break

    starts = {(sy, sx)}

    n_spread = 2
    for i in range(1, h * n_spread + 1):
        newstarts = set()
        for start_tile in starts:
            for ngb in get_neighbours_pbc(grid, h, w, *start_tile):
                newstarts.add(ngb)
        starts = newstarts
    
    for i in range(h * n_spread + 1, h * n_spread + sy + 1):
        newstarts = set()
        for start_tile in starts:
            for ngb in get_neighbours_pbc(grid, h, w, *start_tile):
                newstarts.add(ngb)
        starts = newstarts

    counts_by_grid = defaultdict(int)
    for (r, c) in starts:
        jgrid = r // h
        igrid = c // w
        counts_by_grid[(jgrid, igrid)] += 1

    count_odd = counts_by_grid[(0, 0)]
    count_even = counts_by_grid[(1, 0)]

    if i % 2 == 0:
        count_odd, count_even = count_even, count_odd

    def sum_up(indices):
        return sum(counts_by_grid[ind] for ind in indices)
    
    count_edge1 = sum_up([(-2, -1), (-2, 1), (2, -1), (2, 1)])
    count_edge2 = sum_up([(-1, -1), (-1, 1), (1, -1), (1, 1)])
    count_crnr  = sum_up([( 0, -2), ( 0, 2), (-2, 0), (2, 0)])

    n_grids = n_steps // w
    remainder = (n_steps - sx) % w
    assert remainder == 0, "Does not work for remainder != 0"

    n_odd   = (n_grids - 1)**2
    n_even  =  n_grids**2
    n_edge1 =  n_grids
    n_edge2 = (n_grids - 1)

    #   *^*    ^, >, v, < are corners
    #  */o\*   * is edge type 1
    # *<oeo>*  /\ are edge type 2
    #  *\o/*   o, e are alternating-parity filled grids
    #   *v*
    count = n_odd * count_odd + n_even * count_even \
        + n_edge1 * count_edge1 + n_edge2 * count_edge2 + count_crnr
    if n_steps == h * n_spread + sy:
        assert count == sum(counts_by_grid.values()), "Broken for example"
    return count

if __name__ == "__main__":    
    print("Part 1 example", day21_part1("input/day21_example.txt", 6))
    print("Part 1", day21_part1("input/day21.txt", 64))
    print("Part 2 example", day21_part2("input/day21.txt", 131*2+65))
    print("Part 2", day21_part2("input/day21.txt", 26501365))
    
