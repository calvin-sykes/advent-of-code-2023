from collections import defaultdict, deque, Counter
from tqdm import tqdm
from random import sample

def day25_part1(filename):
    with open(filename) as f:
        lines = map(lambda s: s.rstrip("\n"), f.readlines())

    nodes = set()
    graph = defaultdict(set)
    for l in lines:
        node, edges = l.split(":")
        edges = edges.split()
        nodes.add(node)
        for e in edges:
            graph[node].add(e)
            graph[e].add(node)
    nodes = list(nodes)

    npairs = 1000
    paths = []
    for i in range(npairs):
        start, end = sample(nodes, 2)
        paths.append((start, end))

    visited = Counter()
    for start_node, end_node in paths:
        seen = set()
        stack = deque()
        stack.append(start_node)

        while stack:
            node = stack.popleft()
            seen.add(node)
            if node == end_node:
                break
            for next_node in graph[node]:
                if next_node not in seen:
                    visited[frozenset((node, next_node))] += 1
                    stack.append(next_node)

    top_three = visited.most_common(3)
    for edge in top_three:
        a, b = edge[0]
        graph[a].remove(b)
        graph[b].remove(a)

    in_a = set((a,))
    in_b = set((b,))

    for start_node, subset in zip([a, b], [in_a, in_b]):
        stack = deque()
        stack.append(start_node)

        while stack:
            node = stack.popleft()
            subset.add(node)

            for next_node in graph[node]:
                if next_node not in subset:
                    stack.append(next_node)

    assert in_a != in_b
    return len(in_a) * len(in_b)

if __name__ == "__main__":    
    print("Part 1 example", day25_part1("input/day25_example.txt"))
    print("Part 1", day25_part1("input/day25.txt"))
