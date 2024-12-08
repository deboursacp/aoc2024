from collections import defaultdict
from itertools import combinations

MAP = defaultdict(list)
for i, r in enumerate(open("in.txt")):
    for j, freq in enumerate(r.strip()):
        if freq != ".":
            MAP[freq].append(complex(i, j))
ROWS, COLS = i, j

antinodes: set[complex] = set()
for freq, locs in MAP.items():
    for c in combinations(locs, 2):
        d = c[0] - c[1]
        antinodes.add(c[0] + d)
        antinodes.add(c[0] - 2 * d)
antinodes = list(a for a in antinodes if 0 <= a.imag <= ROWS and 0 <= a.real <= COLS)
print(len(antinodes))
