def parse_seeds_part1(lines):
    seed_str = lines[0].split(":")[-1]
    seeds = list(map(int, seed_str.split()))
    return seeds

def parse_seeds_part2(lines):
    seed_str = lines[0].split(":")[-1]
    seeds = list(map(int, seed_str.split()))

    seed_ranges = []
    for s, ns in zip(seeds[::2], seeds[1::2]):
        seed_ranges.append(range(s, s+ns))
    return seed_ranges

def parse_maps(lines):
    map_starts = []
    for il, l in enumerate(lines[1:], 1):
        if "map" in l:
            map_starts.append(il)
    map_starts.append(len(lines))

    maps = {}
    for im in range(len(map_starts) - 1):
        ms = map_starts[im]
        src, _, dest = lines[ms].split()[0].split("-")
        maps[(src, dest)] = []
        for l in lines[ms+1:map_starts[im+1]-1]:
            maps[(src, dest)].append(tuple(map(int, l.split())))
    return maps

def lookup(the_map, seed):
    for the_range in the_map:
        dest_start, src_start, length = the_range
        if seed in range(src_start, src_start + length):
            return dest_start + (seed - src_start)
    return seed

def lookup_reverse(the_map, location):
    for the_range in the_map:
        dest_start, src_start, length = the_range
        if location in range(dest_start, dest_start + length):
            return src_start + (location - dest_start)
    return location


def day5_part1(filename):
    with open(filename) as f:
        l = f.readlines()

    seeds = parse_seeds_part1(l)
    maps = parse_maps(l)
    locations = []
    
    for seed in seeds:
        map_input = seed
        for mapping in maps:
            map_output = lookup(maps[mapping], map_input)
            map_input = map_output
        locations.append(map_output)
    return min(locations)    

def day5_part2(filename):
    with open(filename) as f:
        l = f.readlines()

    seed_ranges = parse_seeds_part2(l)
    maps = parse_maps(l)

    def bruteforce_reverse(first_loc, loc_step, max_loc):
        location = first_loc
        while location < max_loc:
            if location % 1000 * loc_step == 0:
                print(location, end="\r")
            map_input = location
            for mapping in reversed(maps):
                map_output = lookup_reverse(maps[mapping], map_input)
                map_input = map_output
            seed = map_output
            if seed == location:
                return seed
            for sr in seed_ranges:
                if seed in sr:
                    return location
            location += loc_step

    step = int(1e6)
    limit = int(1e10)
    first = 0
    while True:
        limit = bruteforce_reverse(first, step, limit)
        if step == 1:
            return limit
        else:
            first = limit - step
            step //= 10

if __name__ == "__main__":
    print("Part 1 example", day5_part1("input/day5_example.txt"))
    print("Part 1", day5_part1("input/day5.txt"))
    print("Part 2 example", day5_part2("input/day5_example.txt"))
    print("Part 2", day5_part2("input/day5.txt"))

    
