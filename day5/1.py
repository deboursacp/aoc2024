import graphlib
from collections import defaultdict

predecessors = defaultdict(list)
updates = []
with open("in.txt") as f:
    for l in f.read().splitlines():
        if len(l) == 5:
            # Is a node (all pages are 2 digits, by inspection)
            predecessor, node = map(int, l.split("|"))
            predecessors[node].append(predecessor)
        elif l:  # skip the empty line
            updates.append(list(map(int, l.split(","))))


def is_correct(update: list[int]) -> bool:
    relevant_dag = {
        page: [p for p in predecessors[page] if p in update] for page in update
    }
    topo_order = tuple(graphlib.TopologicalSorter(relevant_dag).static_order())
    topo_idxs = [topo_order.index(page) for page in update]
    # check for monotonic increase
    return all(d2 - d1 > 0 for d2, d1 in zip(topo_idxs[1:], topo_idxs))


def get_middle_element(l: list[int]) -> int:
    return l[len(l) // 2]


tot = sum(get_middle_element(u) for u in updates if is_correct(u))
print(tot)
