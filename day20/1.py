from collections import defaultdict
from collections import defaultdict
import tqdm
from typing import Iterable
from copy import deepcopy

MAP = {
    complex(i, j): val
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}

# For each coord, make 4 cheats (each direction) and check it's in the map.
START = [k for k, v in MAP.items() if v == "S"][0]
END = [k for k, v in MAP.items() if v == "E"][0]
DIRS = [1, -1, 1j, -1j]


def bfs(maze: dict) -> list[complex]:
    # Performs BFS to find the distance to the exit
    visited: set[complex] = set()
    q: list[tuple[complex, list[complex]]] = []
    q.append((START, [START]))
    while q:
        s, path = q.pop(0)
        if s == END:
            return path
        for d in DIRS:
            n = s + d
            if maze.get(n, "#") != "#" and n not in visited:
                q.append((n, path + [n]))
                visited.add(n)
    return -1


# I think this is a bit faster (60it/s vs ~10it/s if we store the path in the queue)
def bfs_fast(maze) -> int:
    # Performs BFS to find the distance to the exit
    visited: set[complex] = set()
    q = []
    q.append((START, 0))
    while q:
        s, depth = q.pop(0)
        if s == END:
            return depth
        for d in DIRS:
            n = s + d
            if maze.get(n, "#") != "#" and n not in visited:
                q.append((n, depth + 1))
                visited.add(n)
    return -1


path = bfs(MAP)
path_len = len(path) - 1  # We include start in path so we can cheat from there.


def cheats() -> Iterable[complex]:
    for start in path:
        for dir in DIRS:
            cheat = start + dir
            if MAP.get(cheat, ".") == "#":
                yield cheat


savings_to_cheats = defaultdict(list)

for cheat in tqdm.tqdm(set(cheats())):
    maze = deepcopy(MAP)
    maze[cheat] = "."
    cheat_path_len = bfs_fast(maze)
    if cheat_path_len > 0:
        savings_to_cheats[path_len - cheat_path_len].append(cheat)

savings_agg = {k: len(v) for k, v in savings_to_cheats.items() if k > 0}

sum(v for k, v in savings_agg.items() if k >= 100)
