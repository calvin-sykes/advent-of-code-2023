from itertools import pairwise
import numpy as np
from collections import namedtuple

Hailstone = namedtuple("Hailstone", ["pos", "vel"])

def find_intersection(h1, h2, ignore_z):
    A = np.column_stack([h1.vel, -h2.vel])
    b = h2.pos - h1.pos
    if ignore_z:
        A = A[:2]
        b = b[:2]
        try:
            tu = np.linalg.solve(A, b)
            if not np.allclose(A @ tu, b):
               return None
            else:
                return tu
        except np.linalg.LinAlgError:
            return None
    else:
        tu, err, rank, *_ = np.linalg.lstsq(A, b, rcond=None)
        return tu if rank == 2 else None

def day24_part1(filename, xy_bounds):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())

    hailstones = []
    for l in lines:
        pos_str, vel_str = l.split("@")
        pos = np.array([int(val) for val in pos_str.split(",")])
        vel = np.array([int(val) for val in vel_str.split(",")])
        hailstones.append(Hailstone(pos, vel))

    intersections = []
    for i, h1 in enumerate(hailstones):
        for h2 in hailstones[i+1:]:
            tu = find_intersection(h1, h2, ignore_z=True)
            if tu is None:
                continue
            if np.any(tu < 0):
                continue
            intersect_pos = h1.pos[:2] + h1.vel[:2] * tu[0]
            if np.any((intersect_pos < xy_bounds[0])|(intersect_pos > xy_bounds[1])):
                continue
            intersections.append(intersect_pos)

    return len(intersections)

def offset_velocities(hailstones, vel):
    relative_stones = []
    vel = np.asarray(vel)
    for h in hailstones:
        relative_stones.append(Hailstone(h.pos, h.vel - vel))
    return relative_stones

def is_possible(hailstones, vprop, component):
    for i, h1 in enumerate(hailstones):
        x1 = h1.pos[component]
        v1 = h1.vel[component]
        for h2 in hailstones[i+1:]:
            x2 = h2.pos[component]
            v2 = h2.vel[component]
            if x1 < x2 and v1 < vprop and vprop < v2:
                return False
    return True

def check_intercepts(hailstones, ignore_z):
    ipt = None
    for h1, h2 in pairwise(hailstones):
        tu = find_intersection(h1, h2, ignore_z)
        if tu is None:
            return None
        intersect_pos = h1.pos + h1.vel * tu[0]
        if ignore_z:
            intersect_pos = intersect_pos[:2]
        if ipt is None:
            ipt = intersect_pos
        else:
            if not np.allclose(ipt, intersect_pos):
                return None
    return ipt

def day24_part2(filename, search_range):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())

    hailstones = []
    for l in lines:
        pos_str, vel_str = l.split("@")
        pos = np.array([int(val) for val in pos_str.split(",")])
        vel = np.array([int(val) for val in vel_str.split(",")])
        hailstones.append(Hailstone(pos, vel))

    rge = search_range
    possible_vx = [x for x in range(-rge, rge) if is_possible(hailstones, x, 0)]
    possible_vy = [y for y in range(-rge, rge) if is_possible(hailstones, y, 1)]
    possible_vz = [z for z in range(-rge, rge) if is_possible(hailstones, z, 2)]
    n_possible = len(possible_vx) * len(possible_vy) * len(possible_vz)

    for vx in possible_vx:
        for vy in possible_vy:
            for vz in possible_vz:
                velocity = np.array([vx, vy, vz])
                relative_stones = offset_velocities(hailstones, velocity)
                isecs = check_intercepts(relative_stones, ignore_z=False)
                if isecs is not None:
                    thrown = Hailstone(isecs, velocity)
                    for h in hailstones:
                        assert find_intersection(h, thrown, False) is not None
                    return sum(isecs).astype(int)

    assert False, "No solution found"
    return None
    
if __name__ == "__main__":    
    print("Part 1 example", day24_part1("input/day24_example.txt", (7, 27)))
    print("Part 1", day24_part1("input/day24.txt", (200000000000000, 400000000000000)))
    print("Part 2 example", day24_part2("input/day24_example.txt", 10))
    print("Part 2", day24_part2("input/day24.txt", 300))
