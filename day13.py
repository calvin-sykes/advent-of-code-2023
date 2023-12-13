from itertools import chain

def find_mirrors(pattern):
    # Check vertical
    ncol = len(pattern[0])
    for i in range(1, ncol):
        mirrored = True
        for l in pattern:
            nleft = i
            nright = ncol - i
            nm = min(nleft, nright)
            
            left = l[i-nm:i]
            right = l[i:i+nm]
            if left != right[::-1]:
                mirrored = False
                break
        if mirrored:
            return ("v", i)

    # Check horizontal
    nrow = len(pattern)
    for i in range(1, nrow):
        mirrored = True
        ntop = i
        nbot = nrow - i
        nm = min(ntop, nbot)
            
        top = pattern[i-nm:i]
        bot = pattern[i:i+nm]
        if any(lt != lb for lt, lb in zip(top, bot[::-1])):
            mirrored = False
            continue
        if mirrored:
            return ("h", i)

    print("\n".join(pattern))
    raise ValueError("No line of reflection found")
    

def find_mirrors_smudged(pattern):
    # Check vertical
    ncol = len(pattern[0])
    for i in range(1, ncol):
        left = []
        right = []
        for l in pattern:
            nleft = i
            nright = ncol - i
            nm = min(nleft, nright)
            left.append(l[i-nm:i])
            right.append(l[i:i+nm][::-1])
        ndiff = 0
        for cl, cr in zip(chain.from_iterable(left), chain.from_iterable(right)):
            ndiff += (cl != cr)
            if ndiff > 1:
                break
        if ndiff == 1:
            return ("v", i)

    # Check horizontal
    nrow = len(pattern)
    for i in range(1, nrow):
        mirrored = True
        ntop = i
        nbot = nrow - i
        nm = min(ntop, nbot)
            
        top = pattern[i-nm:i]
        bot = pattern[i:i+nm]

        ndiff = 0
        for ct, cb in zip(chain.from_iterable(top), chain.from_iterable(bot[::-1])):
            ndiff += (ct != cb)
            if ndiff > 1:
                break
        if ndiff == 1:
            return ("h", i)

    print("\n".join(pattern))
    raise ValueError("No line of reflection found")

def day13_part1(filename):
    with open(filename) as f:
        lines = f.read()
        mirrors = lines.split("\n\n")
        mirrors = list(map(lambda s: s.split("\n"), mirrors))
        mirrors[-1] = mirrors[-1][:-1] #  remove trailing newline
    
    result = 0
    for m in mirrors:
        dirn, pos = find_mirrors(m)
        if dirn == "v":
            result += pos
        else:
            result += pos * 100
        
    return result

def day13_part2(filename):
    with open(filename) as f:
        lines = f.read()
        mirrors = lines.split("\n\n")
        mirrors = list(map(lambda s: s.split("\n"), mirrors))
        mirrors[-1] = mirrors[-1][:-1] #  remove trailing newline
    
    result = 0
    for m in mirrors:
        dirn, pos = find_mirrors_smudged(m)
        if dirn == "v":
            result += pos
        else:
            result += pos * 100
        
    return result

if __name__ == "__main__":
    print("Part 1 example", day13_part1("input/day13_example.txt"))
    print("Part 1", day13_part1("input/day13.txt"))
    print("Part 2 example", day13_part2("input/day13_example.txt"))
    print("Part 2", day13_part2("input/day13.txt"))
