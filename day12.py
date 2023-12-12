from functools import cache

@cache
def spring_combinations(springs, counts):
    if len(counts) == 0:
        return "#" not in springs

    ccount = 0

    # Take first damaged group, slide along string testing for valid placement
    n = counts[0]
    for i in range(len(springs)):
        if "." in springs[i:i+n]: # Cannot place on an known good tile
            continue
        elif i > len(springs) - n: # Not enough space for group
            continue
        elif i + n < len(springs) and springs[i+n] == "#": # Extra damaged after
            continue
        elif i > 0 and "#" in springs[:i]: # Extra damaged before
            continue
        ccount += spring_combinations(springs[i+n+1:], counts[1:])
    return ccount
        
def unfold(springs, counts, factor=5):
    return (
        "?".join((springs,)*factor),
        counts*factor
    )

def day12_part1(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))

    spring_data = []
    for l in lines:
        springs, counts = l.split(" ")
        counts = tuple(map(int, counts.split(",")))
        spring_data.append((springs, counts))
    
    sum = 0
    for springs, counts in spring_data:
        s = spring_combinations(springs, counts)
        spring_combinations.cache_clear()
        sum += s
        
    return sum

def day12_part2(filename):
    with open(filename) as f:
        lines = list(map(lambda l: l.rstrip("\n"), f.readlines()))

    spring_data = []
    for l in lines:
        springs, counts = l.split(" ")
        counts = tuple(map(int, counts.split(",")))
        spring_data.append((springs, counts))

    sum = 0
    for springs, counts in spring_data:
        usprings, ucounts = unfold(springs, counts, 5)
        s = spring_combinations(usprings, ucounts)
        spring_combinations.cache_clear()
        sum += s
        
    return sum

if __name__ == "__main__":
    print("Part 1 example", day12_part1("input/day12_example.txt"))
    print("Part 1", day12_part1("input/day12.txt"))
    print("Part 2 example", day12_part2("input/day12_example.txt"))
    print("Part 2", day12_part2("input/day12.txt"))
