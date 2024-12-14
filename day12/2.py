from collections import defaultdict
from dataclasses import dataclass
import itertools

MAP = {
    complex(i, j): val
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}
DIRECTIONS = [1, -1, 1j, -1j]


@dataclass
class Region:
    crop_type: str
    plots: set[complex]
    edges: dict[complex, set]

    def cost_1(self):
        return self.area * self.num_edges

    def cost_2(self):
        return self.area * self.count_sides()

    @property
    def area(self):
        return len(self.plots)

    @property
    def num_edges(self):
        return sum(len(v) for v in self.edges.values())

    def count_sides(self) -> int:
        adjacent_edges = 0
        for edges in self.edges.values():
            for a, b in itertools.combinations(edges, 2):
                # Instead of o(n^2) combinations, we could group,sort, and compare neighbors.
                # ... but this seems efficient enough for the input size, it runs in <1s.
                if (a.real == b.real and abs(a.imag - b.imag) == 1) or (
                    a.imag == b.imag and abs(a.real - b.real) == 1
                ):
                    adjacent_edges += 1
        return self.num_edges - adjacent_edges


seen: set[complex] = set()
regions: list[Region] = []
for loc, crop_type in MAP.items():
    if loc in seen:
        continue
    region: set[complex] = set()

    edges: dict[complex, set] = defaultdict(set)
    # Traverse the contiguous region.
    q = set([loc])
    while q:
        s = q.pop()
        seen.add(s)
        region.add(s)
        for dir in DIRECTIONS:
            next = s + dir
            if next in MAP and next not in seen and MAP[next] == crop_type:
                q.add(next)
            if MAP.get(next, None) != crop_type:
                # We're at a boundary, add the edge.
                edges[dir].add(s)

    regions.append(Region(crop_type, region, edges))


print(sum([r.cost_1() for r in regions]))
print(sum([r.cost_2() for r in regions]))
