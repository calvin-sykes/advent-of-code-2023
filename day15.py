def HASH(string):
    val = 0
    for c in string:
        val += ord(c)
        val *= 17
        val = val % 256
    return val

class Box:
    def __init__(self, index):
        self.i = index
        self.labels = []
        self.lenses = []

    def __contains__(self, label):
        return label in self.labels

    def __getitem__(self, label):
        try:
            i = self.labels.index(label)
        except ValueError as e:
            raise KeyError(f"Label '{label} not in box")
        return (label, self.lenses[i])

    def __setitem__(self, label, lens):
        try:
            i = self.labels.index(label)
        except ValueError as e:
            self.add(label, lens)
        else:
            self.lenses[i] = lens

    def __len__(self):
        return len(self.labels)
    
    def __repr__(self):
        if len(self):
            box_repr = f"Box {self.i}: "
            for label, lens in zip(self.labels, self.lenses):
                box_repr += f"[{label} {lens}] "
            return box_repr
        else:
            return f"Box {self.i}: (empty)"

    def add(self, label, lens):
        self.labels.append(label)
        self.lenses.append(lens)

    def remove(self, label):
        try:
            i = self.labels.index(label)
        except IndexError as e:
            pass
        self.labels.remove(label)
        return self.lenses.pop(i)

    def power(self):
        if not len(self):
            return 0
        return sum((self.i + 1) * (il + 1) * lens for il, lens in enumerate(self.lenses))

def print_boxes(boxes):
    for b in boxes:
        if len(b):
            print(b)

def day15_part1(filename):
    with open(filename) as f:
        seq = f.read().rstrip("\n").split(",")

    return sum(HASH(s) for s in seq)

def day15_part2(filename):
    with open(filename) as f:
        seq = f.read().rstrip("\n").split(",")

    boxes = [Box(i) for i in range(256)]

    for step in seq:
        equals = "=" in step
        if equals:
            label, focal_length = step.split("=")
            focal_length = int(focal_length)
        else:
            label = step.rstrip("-")
        b = HASH(label)

        if equals:
            boxes[b][label] = focal_length
        else:
            if label in boxes[b]:
                boxes[b].remove(label)

    #print_boxes(boxes)
    return sum(b.power() for b in boxes)

if __name__ == "__main__":
    print("Part 1 example", day15_part1("input/day15_example.txt"))
    print("Part 1", day15_part1("input/day15.txt"))
    print("Part 2 example", day15_part2("input/day15_example.txt"))
    print("Part 2", day15_part2("input/day15.txt"))
