import re

class Condition:
    def __init__(self, catg, cond, val):
        if cond == ">":
            self.f = lambda r: r[catg] > int(val)
        elif cond == "<":
            self.f = lambda r: r[catg] < int(val)
        elif cond == "Always":
            self.f = lambda _: True
        else:
            raise ValueError

        self.catg = catg
        self.val = int(val) if val is not None else None
        self.greater = cond == ">"

        if cond == "Always":
            self.cond_str = cond
        else:
            self.cond_str = catg + cond + val

    def __call__(self, r):
        return self.f(r)

    def __repr__(self):
        return self.cond_str

def day19_part1(filename):
    with open(filename) as f:
        workflows_in, ratings_in = map(lambda s: s.split("\n"),
                                       f.read().split("\n\n"))

    rules_re = re.compile(r"([a-z])(<|>)(\d+):([a-z]+|(?:A|R))")
    workflows = dict()
    for wf in workflows_in:
        name, rules_in = wf.split("{")
        rules_in = rules_in.rstrip("}").split(",")

        transitions = []
        for r in rules_in:
            if match := re.search(rules_re, r):
                catg, cond, val, state = match.groups()
                cond_fn = Condition(catg, cond, val)
                transitions.append({"cond": cond_fn, "state": state})
        cond_fn = Condition(None, "Always", None)
        transitions.append({"cond": cond_fn, "state": rules_in[-1]})
        workflows[name] = transitions

    ratings_re = re.compile(r"(x|m|a|s)=(\d+)")
    ratings = []
    for r in ratings_in[:-1]:
        part = {}
        for catg, val in re.findall(ratings_re, r):
            part[catg] = int(val)
        ratings.append(part)

    accepted = []
    for part in ratings:
        wf = "in"
        while True:
            for rule in workflows[wf]:
                if rule["cond"](part) == True:
                    wf = rule["state"]
                    break
            if wf == "R":
                break
            elif wf == "A":
                accepted.append(part)
                break

    return sum(sum(part.values()) for part in accepted)

accepted = []

def find_bounds(workflows, wf, bounds):
    total = 0
    for rule in workflows[wf]:
        cond = rule["cond"]
        catg = cond.catg
        if catg is None: # Always
            rge1 = {catg: bounds[catg] for catg in bounds}
            rge2 = {catg: [0, 0] for catg in bounds}
        else:
            if cond.greater:
                rge1 = {catg: [cond.val+1, bounds[catg][1]]}
                rge2 = {catg: [bounds[catg][0], cond.val]}
            else:
                rge1 = {catg: [bounds[catg][0], cond.val-1]}
                rge2 = {catg: [cond.val, bounds[catg][1]]}
        b1 = bounds | rge1
        b2 = bounds | rge2
        if rule["state"] == "A":
            lengths = [b[1] - b[0] + 1 for b in b1.values()]
            acc = lengths[0]
            for l in lengths[1:]:
                acc *= l
            accepted.append((b1, acc))
            total += acc
        elif rule["state"] == "R":
            pass
        else:
            total += find_bounds(workflows, rule["state"], b1)
        bounds = b2
    return total
            
def day19_part2(filename):
    with open(filename) as f:
        workflows_in, ratings_in = map(lambda s: s.split("\n"),
                                       f.read().split("\n\n"))

    rules_re = re.compile(r"([a-z])(<|>)(\d+):([a-z]+|(?:A|R))")
    workflows = dict()
    for wf in workflows_in:
        name, rules_in = wf.split("{")
        rules_in = rules_in.rstrip("}").split(",")

        transitions = []
        for r in rules_in:
            if match := re.search(rules_re, r):
                catg, cond, val, state = match.groups()
                cond_fn = Condition(catg, cond, val)
                transitions.append({"cond": cond_fn, "state": state})
        cond_fn = Condition(None, "Always", None)
        transitions.append({"cond": cond_fn, "state": rules_in[-1]})
        workflows[name] = transitions

    bounds = {catg: [1, 4000] for catg in "xmas"}
    return find_bounds(workflows, "in", bounds)

if __name__ == "__main__":
    print("Part 1 example", day19_part1("input/day19_example.txt"))
    print("Part 1", day19_part1("input/day19.txt"))
    print("Part 2 example", day19_part2("input/day19_example.txt"))
    print("Part 2", day19_part2("input/day19.txt"))
