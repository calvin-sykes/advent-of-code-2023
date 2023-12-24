from operator import attrgetter
from itertools import groupby
from collections import defaultdict, deque

def plot(bricks, axis):
    maxx = maxy = maxz = 0
    for b in bricks:
        maxx = max(maxx, b.x2)
        maxy = max(maxy, b.y2)
        maxz = max(maxz, b.z2)
    if axis == "x":
        grid = [["." for _ in range(maxx+1)] for __ in range(maxz)]
        grid.append(["-"] * (maxx + 1))
        for b in bricks:
            for z in range(b.z1, b.z2 + 1):
                for x in range(b.x1, b.x2 + 1):
                    grid[maxz-z][x] = b.id if grid[maxz-z][x] == "." else "?"
    elif axis == "y":
        grid = [["." for _ in range(maxy+1)] for __ in range(maxz)]
        grid.append(["-"] * (maxy + 1))
        for b in bricks:
            for z in range(b.z1, b.z2 + 1):
                for y in range(b.y1, b.y2 + 1):
                    grid[maxz-z][y] = b.id if grid[maxz-z][y] == "." else "?"
    return f"axis={axis}\n" + "\n".join("".join(l) for l in grid)
        
class Brick:
    ID = ord("A")
    def __init__(self, start, end):
        start = list(start)
        end = list(end)
        assert all(e >= s for s, e in zip(start, end))
        self.x1, self.y1, self.z1 = start
        self.x2, self.y2, self.z2 = end
        self.lx, self.ly, self.lz = (e - s + 1 for s, e in zip(start, end))
        assert sum((self.lx > 1, self.ly > 1, self.lz > 1)) <= 1, (self.lx, self.ly, self.lz)
        self.id = chr(Brick.ID)
        Brick.ID += 1

    def __repr__(self):
        return f"Brick(({self.x1}, {self.y1}, {self.z1}), ({self.x2}, {self.y2}, {self.z2}), ID={self.id} ({ord(self.id)}))"

    def __contains__(self, pt):
        x, y, z = pt
        if self.x1 > x or self.x2 < x:
            return False
        if self.y1 > y or self.y2 < y:
            return False
        if self.z1 > z or self.z2 < z:
            return False
        return True

    @property
    def blocks(self):
        if self.lx > 1:
            blocks = ((x, self.y1, self.z1) for x in range(self.x1, self.x2+1))
        elif self.ly > 1:
            blocks = ((self.x1, y, self.z1) for y in range(self.y1, self.y2+1))
        else:
            blocks = ((self.x1, self.y1, self.z1),)
        return list(blocks)

    def supports(self, other):
        return any((bx, by, bz-1) in self for (bx, by, bz) in other.blocks)

    def can_fall(self, bricks_below):
        if self.z1 == 1:
            return False
        for brick in bricks_below:
            if brick == self:
                continue
            if brick.z1 > self.z2 or brick.z2 < self.z1 - 1:
                continue
            if brick.supports(self):
                return False
        return True

def let_bricks_fall(bricks, ret_nfall=False):
    grouped_by_z = defaultdict(set)
    for attr in ["z2", "z1"]:
        key_func = attrgetter(attr)
        sorted_by_z = sorted(bricks, key=key_func)
        for z, bb in groupby(sorted_by_z, key=key_func):
            grouped_by_z[z] |= set(bb)

    fell = set()
    for brick in sorted_by_z:
        while brick.z1 > 1:
            z = brick.z1
            if brick.can_fall(grouped_by_z[z-1]):
                fell.add(brick)
                grouped_by_z[z].remove(brick)
                if brick.lz > 1:
                    grouped_by_z[z+brick.lz-1].remove(brick)
                grouped_by_z[z-1].add(brick)
                if brick.lz > 1:
                    grouped_by_z[z+brick.lz-2].add(brick)
                brick.z1 -= 1
                brick.z2 -= 1
            else:
                break
    if ret_nfall:
        return (grouped_by_z, len(fell))
    else:
        return grouped_by_z
    
def day22_part1(filename):
    with open(filename) as f:
        lines = f.readlines()

    Brick.ID = ord("A")
    bricks = []
    for l in lines:
        start, end = map(lambda s: s.split(","), l.split("~"))
        bricks.append(Brick(map(int, start), map(int, end)))

    grouped_by_z = let_bricks_fall(bricks)
    assert let_bricks_fall(bricks, True)[1] == 0

    supported_by = defaultdict(set)
    supports = defaultdict(set)
    for brick in bricks:
        if brick.z1 == 1:
            continue
        for other in grouped_by_z[brick.z1-1]:
            assert other.id != brick.id
            if other.supports(brick):
                supports[other.id].add(brick)
                supported_by[brick.id].add(other)

    can_be_deleted = set()
    for b in bricks:
        if b.id not in supports:
            can_be_deleted.add(b)
        if len(supported_by[b.id]) > 1:
            for b2 in supported_by[b.id]:
                if all(len(supported_by[b3.id]) > 1 for b3 in supports[b2.id]):
                    can_be_deleted.add(b2)

    return len(can_be_deleted)

def day22_part2(filename):
    with open(filename) as f:
        lines = f.readlines()

    Brick.ID = ord("A")
    bricks = []
    for l in lines:
        start, end = map(lambda s: s.split(","), l.split("~"))
        bricks.append(Brick(map(int, start), map(int, end)))

    grouped_by_z = let_bricks_fall(bricks)

    supported_by = defaultdict(set)
    supports = defaultdict(set)
    for brick in bricks:
        if brick.z1 == 1:
            continue
        for other in grouped_by_z[brick.z1-1]:
            assert other.id != brick.id
            if other.supports(brick):
                supports[other.id].add(brick)
                supported_by[brick.id].add(other)

    can_be_deleted = set()
    for b in bricks:
        if b.id not in supports:
            can_be_deleted.add(b)
        if len(supported_by[b.id]) > 1:
            for b2 in supported_by[b.id]:
                if all(len(supported_by[b3.id]) > 1 for b3 in supports[b2.id]):
                    can_be_deleted.add(b2)

    causes_chain_reaction = set(bricks) - can_be_deleted

    chain_reaction = defaultdict(set)
    for brick in causes_chain_reaction:
        stack = deque()
        stack.append(brick)
        while stack:
            b = stack.pop()
            if b != brick:
                chain_reaction[brick.id].add(b)
            for b2 in supports[b.id]:
                if (len(supported_by[b2.id]) == 1) or \
                   all(b3 in chain_reaction[brick.id] for b3 in supported_by[b2.id]):
                    if b2 not in chain_reaction[brick.id]:
                        stack.append(b2)
    return sum(len(chain_reaction[brick_id]) for brick_id in chain_reaction)

if __name__ == "__main__":    
    print("Part 1 example", day22_part1("input/day22_example.txt"))
    print("Part 1", day22_part1("input/day22.txt"))
    print("Part 2 example", day22_part2("input/day22_example.txt"))
    print("Part 2", day22_part2("input/day22.txt"))
