from collections import defaultdict
from itertools import combinations

MAP = defaultdict(list)
for i, r in enumerate(open("ex.txt")):
    for j, freq in enumerate(r.strip()):
        if freq != ".":
            MAP[freq].append(complex(i, j))
ROWS, COLS = i, j
inbounds = lambda pos: (0 <= pos.imag <= ROWS and 0 <= pos.real <= COLS)
antinodes: set[complex] = set()
for freq, locs in MAP.items():
    for ant1, ant2 in combinations(locs, 2):
        d = ant1 - ant2
        while inbounds(ant1):
            antinodes.add(ant1)
            ant1 += d
        while inbounds(ant2):
            antinodes.add(ant2)
            ant2 -= d

print(len(antinodes))
