from sympy import symbols, solve

import re


class Machine:
    def __init__(self, line):
        a1, a2, b1, b2, t1, t2 = map(int, re.findall(r"(\d+)", line))
        self.A, self.B = symbols("A B")
        self.eq1 = a1 * self.A + b1 * self.B - t1
        self.eq2 = a2 * self.A + b2 * self.B - t2
        # Yeah... sympy is probably cheating. I could do math.lcm(a1,a2) and write my own solver too.
        self.solution = solve((self.eq1, self.eq2), (self.A, self.B))

    @property
    def is_solvable(self) -> bool:
        return self.solution[self.A].is_Integer and self.solution[self.B].is_Integer

    @property
    def cost(self) -> int:
        if not self.is_solvable:
            return 0
        return 3 * self.solution[self.A] + self.solution[self.B]


with open("in.txt") as f:
    machines = [Machine(l) for l in f.read().split("\n\n")]
sum(m.cost for m in machines)
