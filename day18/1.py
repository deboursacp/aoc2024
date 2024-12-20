is_ex = False

bts = [
    tuple(map(int, l.split(",")))
    for l in open("ex.txt" if is_ex else "in.txt").readlines()
]
DIM = 7 if is_ex else 71
NUM_OBSTACLES = 12 if is_ex else 1024
START = (0, 0)
EXIT = (DIM - 1, DIM - 1)
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
add = lambda a, b: (a[0] + b[0], a[1] + b[1])
# X,Y coordinate, where X is the distance from the left edge of your memory space
# and Y is the distance from the top edge of your memory space.
GRID = {(x, y): "." for x in range(DIM) for y in range(DIM)}
coord = tuple[int, int]


def bfs(grid, start: coord = (0, 0)):
    visited: set[coord] = set()
    q: list[tuple[coord, int]] = []
    q.append((start, 0))
    while q:
        s, dist = q.pop(0)
        if s == EXIT:
            return dist
        for d in DIRS:
            n = add(s, d)
            if grid.get(n, "#") != "#" and n not in visited:
                q.append((n, dist + 1))
                visited.add(n)
    return -1


# print(bfs())  # part 1
from copy import deepcopy
from tqdm import trange

# we could binary search, but i found linear was fast enough
for i in trange(len(bts)):
    grid = deepcopy(GRID)
    for b in bts[:i]:
        grid[b] = "#"

    if bfs(grid) < 0:
        break
print(bts[i - 1])
