"""
p=x,y ; where x represents the number of tiles the robot is from the left wall
"""

IN_DIMS = (101, 103)  # width, height
EX_DIMS = (11, 7)
import re
from collections import Counter
from functools import reduce
from operator import mul

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

    def quadrant(self):
        if self.pos.real == center[0] or self.pos.imag == center[1]:
            return -1
        return int(self.pos.real > center[0]) + 2 * int(self.pos.imag > center[1])


guards = [Guard(l) for l in open(fn).readlines()]
[g.travel(100) for g in guards]
quad_counts = Counter(g.quadrant() for g in guards if g.quadrant() >= 0).values()
score = reduce(mul, quad_counts)
print(score)
