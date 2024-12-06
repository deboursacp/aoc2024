import graphlib
from collections import defaultdict

predecessors = defaultdict(list)
updates = []
with open("in.txt") as f:
    for l in f.read().splitlines():
        if len(l) == 5:
            # Is a node (all pages are 2 digits, from inspection)
            predecessor, node = map(int, l.split("|"))
            predecessors[node].append(predecessor)
        elif l:  # skip the empty line
            updates.append(list(map(int, l.split(","))))


def get_middle_element(l: list[int]) -> int:
    return l[len(l) // 2]


correct_sum, incorrect_sum = 0, 0
for update in updates:
    relevant_dag = {
        page: [p for p in predecessors[page] if p in update] for page in update
    }
    topo_order = tuple(graphlib.TopologicalSorter(relevant_dag).static_order())
    correct_order = [t for t in topo_order if t in update]
    if update == correct_order:
        correct_sum += get_middle_element(update)
    else:
        incorrect_sum += get_middle_element(correct_order)

print(f"{correct_sum=}\n{incorrect_sum=}")
