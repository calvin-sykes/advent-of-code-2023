from collections import defaultdict

from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from sys import maxsize

class D:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass(order=True)
class QueueEntry:
    weight: int
    item: Any = field(compare=False)

class Queue:
    def __init__(self):
        self.q = []
        self.items = {}

    def __len__(self):
        return len(self.items)

    def __contains__(self, item):
        return item in self.items

    def push(self, weight, item):
        entry = QueueEntry(weight, item)
        self.items[item] = entry
        heappush(self.q, entry)

    def pop(self):
        while self.q:
            entry = heappop(self.q)
            item = entry.item
            if item is not None:
                del self.items[item]
                return entry.weight, entry.item
        raise KeyError("Empty queue")

    def get_weight(self, item):
        return self.items[item].weight

    def set_weight(self, new_weight, item):
        entry = self.items.pop(item)
        entry.item = None
        self.push(new_weight, item)

def get_neighbours_restricted(r, c, d, s, h, w):
    MAX_STREAK = 3
    neighbours = []
    for nd, dr, dc in zip(range(4), [-1, 0, 1, 0], [0, 1, 0, -1]):
        nr = r + dr
        nc = c + dc
        ns = s + 1 if nd == d else 1
        if nr == -1 or nr == h or nc == -1 or nc == w:
            continue # OOB
        elif nd == d:
            if s == MAX_STREAK:
                continue # Streak is full
            else:
                neighbours.append((r + dr, c + dc, nd, ns))
        elif nd == ((d + 2) % 4): # Cannot turn around
            continue
        else:
            neighbours.append((r + dr, c + dc, nd, ns))
    return neighbours

def get_neighbours_ultra_restricted(r, c, d, s, h, w):
    MIN_STREAK = 4
    MAX_STREAK = 10
    neighbours = []
    for nd, dr, dc in zip(range(4), [-1, 0, 1, 0], [0, 1, 0, -1]):
        nr = r + dr
        nc = c + dc
        ns = s + 1 if nd == d else 1
        forced = max(0, MIN_STREAK-ns)
        if (nr + dr * forced not in range(0, h)) \
           or (nc + dc * forced not in range(0, w)):
            continue # Will hit wall before minimum streak
        elif nr == -1 or nr == h or nc == -1 or nc == w:
            continue # OOB
        elif nd == d:
            if s == MAX_STREAK:
                continue # Streak is full
            else:
                neighbours.append((r + dr, c + dc, nd, ns))
        elif nd == ((d + 2) % 4): # Cannot turn around
            continue
        elif s >= MIN_STREAK:
            neighbours.append((r + dr, c + dc, nd, ns))
    return neighbours

def shortest_path(grid, er, ec, ngb_func):
    h, w = len(grid), len(grid[0])

    nodes = Queue()
    prev = dict()
    prev[0, 0, D.EAST, 0] = None
    prev[0, 0, D.SOUTH, 0] = None

    dist = defaultdict(lambda: maxsize)
    dist[0, 0, D.EAST, 0] = grid[0][0]
    dist[0, 0, D.SOUTH, 0] = grid[0][0]

    r, c = 0, 0
    er, ec = h - 1, w - 1

    nodes.push(0, (r, c, D.EAST, 0))
    nodes.push(0, (r, c, D.SOUTH, 0))

    while nodes:
        dist_so_far, pt = nodes.pop()
        for ngb in ngb_func(*pt, h, w):
            dist_step = dist_so_far + grid[ngb[0]][ngb[1]]
            if dist_step < dist[ngb]:
                dist[ngb] = dist_step
                prev[ngb] = pt
                if ngb not in nodes:
                    nodes.push(dist[ngb], ngb)
                else:
                    nodes.set_weight(dist[ngb], ngb)

    path = []
    length = 0

    for ngb in prev:
        if ngb[:2] == (er, ec):
            to = ngb
            break

    while to is not None:
        path.append(to)
        if to[:2] == (0, 0):
            break
        length += grid[to[0]][to[1]]
        to = prev[to]

    pathgrid = list()
    for l in grid:
        pathgrid.append([])
        for c in l:
            pathgrid[-1].append(str(c))
    for (r, c, *_) in path:
        pathgrid[r][c] = "."

    #print("\n".join("".join(l) for l in pathgrid))
    #print("->".join(str(ngb[:2]) for ngb in path))
    return length

def day17_part1(filename):
    with open(filename) as f:
        grid = map(list, f.readlines())
        grid = [list(int(c) for c in l[:-1]) for l in grid]
    h, w = len(grid), len(grid[0])

    return shortest_path(grid, h-1, w-1, get_neighbours_restricted)

def day17_part2(filename):
    with open(filename) as f:
        grid = map(list, f.readlines())
        grid = [list(int(c) for c in l[:-1]) for l in grid]
    h, w = len(grid), len(grid[0])

    return shortest_path(grid, h-1, w-1, get_neighbours_ultra_restricted)

if __name__ == "__main__":
    print("Part 1 example", day17_part1("input/day17_example.txt"))
    print("Part 1", day17_part1("input/day17.txt"))
    print("Part 2 example", day17_part2("input/day17_example.txt"))
    print("Part 2 second example", day17_part2("input/day17_example2.txt"))
    print("Part 2", day17_part2("input/day17.txt"))
