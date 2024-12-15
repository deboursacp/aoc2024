"""
p=x,y ; where x represents the number of tiles the robot is from the left wall
"""

IN_DIMS = (101, 103)  # width, height
EX_DIMS = (11, 7)
import re
from tqdm import trange

ex = False
DIMS, fn = (EX_DIMS, "ex.txt") if ex else (IN_DIMS, "in.txt")

center = (DIMS[0] // 2, DIMS[1] // 2)


class Guard:
    def __init__(self, line):
        p0, p1, v0, v1 = map(int, re.findall(r"(-?\d+)", line))
        self.pos = complex(p0, p1)
        self.vel = complex(v0, v1)

    def travel(self, ticks=1):
        new_pos = self.pos + ticks * self.vel
        self.pos = complex(new_pos.real % DIMS[0], new_pos.imag % DIMS[1])


def print_map(guards: list[Guard]):
    grid = [[0] * DIMS[0] for _ in range(DIMS[1])]
    for g in guards:
        grid[int(g.pos.imag)][int(g.pos.real)] += 1
    print("\n".join("".join(str(v or ".") for v in r) for r in grid), "\n")


guards = [Guard(l) for l in open(fn).readlines()]

init_pos = [g.pos for g in guards]
cycle_val = 0
while True:
    [g.travel() for g in guards]
    if [g.pos for g in guards] == init_pos:
        break
    cycle_val += 1


def get_adj_score(guards: list[Guard]):
    # Maybe it'd be a sufficient heuristic to pick an arbitrary guard and find distance then look at top k
    # return sum(abs(g1.pos - g2.pos) for g1, g2 in itertools.combinations(guards, 2))
    g1 = guards[0]
    return sum(abs(g1.pos - g2.pos) for g2 in guards)


print(f"{cycle_val=}")
scores = []
for i in trange(cycle_val):
    scores.append(get_adj_score(guards))
    [g.travel() for g in guards]
most_clustered_idx = scores.index(min(scores))


guards = [Guard(l) for l in open(fn).readlines()]
[g.travel(most_clustered_idx) for g in guards]
print_map(guards)
print(most_clustered_idx)
