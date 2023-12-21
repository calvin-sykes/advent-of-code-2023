from collections import deque, defaultdict
from copy import deepcopy
from math import lcm

LOW = 0
HIGH = 1

NOISY = False

class Pulse:
    def __init__(self, state, src, dest):
        self.state = state
        self.src = src
        self.dst = dest

    def __repr__(self):
        state = "high" if self.state == HIGH else "low"
        return f"{self.src} -{state}-> {self.dst}"

class Module:
    def __init__(self, name, input, output):
        self.name = name
        self.inp  = input
        self.outp = output

    def __eq__(self, other):
        return self.name == other.name and \
            self.inp == other.inp and \
            self.outp == other.outp

    def process_pulse(self, pulse):
        raise NotImplementedError

class BroadcastModule(Module):
    def __init__(self, name, input, output):
        super().__init__(name, input, output)

    def process_pulse(self, pulse):
        return [Pulse(pulse.state, self.name, dst) for dst in self.outp]

class FlipflopModule(Module):
    def __init__(self, name, input, output):
        super().__init__(name, input, output)
        self.state = LOW

    def __eq__(self, other):
        return super().__eq__(other) and self.state == other.state

    def process_pulse(self, pulse):
        if pulse.state == LOW:
            self.state ^= 1
            return [Pulse(self.state, self.name, dst) for dst in self.outp]
        
class ConjunctionModule(Module):
    def __init__(self, name, input, output):
        super().__init__(name, input, output)
        self.mem = {inp: LOW for inp in input}

    def __eq__(self, other):
        return super().__eq__(other) and self.mem == other.mem

    def process_pulse(self, pulse):
        self.mem[pulse.src] = pulse.state
        if all(self.mem[src] == HIGH for src in self.inp):
            state = LOW
        else:
            state = HIGH
        return [Pulse(state, self.name, dst) for dst in self.outp]

class DummyModule(Module):
    states = ["LOW", "HIGH"]
    
    def __init__(self, name, input, output):
        super().__init__(name, input, output)
    
    def process_pulse(self, pulse):
        if NOISY:
            print(f"{self.name} received {self.states[pulse.state]} pulse")

def build_modules(lines):
    module_plan = {}
    for l in lines:
        name, outputs = l.split(" -> ")
        if name[0] == "%":
            module_type = FlipflopModule
            name = name[1:]
        elif name[0] == "&":
            module_type = ConjunctionModule
            name = name[1:]
        elif name == "broadcaster":
            module_type = BroadcastModule
        else:
            module_type = Module
        outputs = list(map(lambda s: s.replace(" ", ""), outputs.split(",")))
        module_plan[name] = {"type": module_type, "output": outputs, "input": list()}

    dummies = {}
    for mod in module_plan:
        for dst in module_plan[mod]["output"]:
            if dst not in module_plan:
                dummies[dst] = {"type": DummyModule, "output": list(), "input": list()}
                dummies[dst]["input"].append(mod)
            else:
                module_plan[dst]["input"].append(mod)
    module_plan.update(dummies)

    modules = {}
    for mod in module_plan:
        module_class = module_plan[mod].pop("type")
        modules[mod] = module_class(name=mod, **module_plan[mod])

    return modules

def run_modules_count(modules, until=1000):
    button_pulse = Pulse(LOW, "button", "broadcaster")

    pulse_count = {LOW: 0, HIGH: 0}
    pulse_stack = deque()

    n_presses = until
    for i in range(n_presses):
        pulse_stack.append(button_pulse)
        pulse_count[LOW] += 1

        while pulse_stack:
            pulse = pulse_stack.popleft()
            output_pulses = modules[pulse.dst].process_pulse(pulse)
            if output_pulses:
                for p in output_pulses:
                    pulse_count[p.state] += 1
                    pulse_stack.append(p)
    return pulse_count
    

def day20_part1(filename):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())

    modules = build_modules(lines)
    pulse_count = run_modules_count(modules, 1000)
    
    return pulse_count[LOW] * pulse_count[HIGH]

def tarjan_connect(modules):
    module_stack = deque()
    index = 0

    indices = defaultdict(lambda: None)
    lowlink = defaultdict(lambda: len(modules)+1)
    onstack = defaultdict(bool)

    components = []
        
    def strong_connect(mod):
        nonlocal index
        indices[mod] = index
        lowlink[mod] = index
        index += 1
        module_stack.append(mod)
        onstack[mod] = True

        for outp in modules[mod].outp:
            if indices[outp] is None:
                strong_connect(outp)
                lowlink[mod] = min(lowlink[mod], lowlink[outp])
            elif onstack[outp]:
                lowlink[mod] = min(lowlink[mod], indices[outp])

        if lowlink[mod] == indices[mod]:
            newcomp = []
            while True:
                outp = module_stack.pop()
                onstack[outp] = False
                newcomp.append(outp)
                if outp == mod:
                    break
            components.append(newcomp)

    for mod in modules:
        if indices[mod] is None:
            strong_connect(mod)

    return components

def day20_part2(filename):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())

    modules = build_modules(lines)
    modules_copy = deepcopy(modules)
    components = [comp for comp in tarjan_connect(modules) if len(comp) > 1]
    ncomp = len(components)

    n_presses = 0
    cycle_lengths = [0] * ncomp
    cycled = [False] * ncomp

    button_pulse = Pulse(LOW, "button", "broadcaster")
    pulse_stack = deque()

    while True:
        pulse_stack.append(button_pulse)
        n_presses += 1

        while pulse_stack:
            pulse = pulse_stack.popleft()
            output_pulses = modules[pulse.dst].process_pulse(pulse)
            if output_pulses:
                for p in output_pulses:
                    pulse_stack.append(p)

        for i, comp in enumerate(components):
            if not cycled[i]:
                cycle_lengths[i] += 1
            if all(modules[mod] == modules_copy[mod] for mod in comp):
                cycled[i] = True
        if all(cycled):
            break
    return lcm(*cycle_lengths)

if __name__ == "__main__":
    print("Part 1 example", day20_part1("input/day20_example.txt"))
    print("Part 1 second example", day20_part1("input/day20_example2.txt"))
    print("Part 1", day20_part1("input/day20.txt"))
    #print("Part 2 example", day20_part2("input/day20_example.txt"))
    print("Part 2", day20_part2("input/day20.txt"))
