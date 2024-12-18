MAP = {
    complex(i, j): val
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}
# DIRECTIONS = [1, -1, 1j, -1j]
STEP_SCORE = 1
TURN_SCORE = 1_000

# Efficiency Ideas:
# If at any point, our score is greater than the lowest score found, return math.inf
# I don't think we can consider heuristics because of the 90 turning...
# You can't double back on yourself, so just neighbors = (curr_dir, curr_dir * 1j, curr_dir * -1j)

# I don't think we can use dijkstra's here since orientation influences things.


from math import inf
from copy import deepcopy
from typing import Optional
import sys

sys.setrecursionlimit(15000)

best_score = inf
best_path = set
best_by_node = {k: inf for k in MAP}


def traverse_all(
    loc: complex,
    orientation: complex = 1j,
    visited: Optional[set] = None,
    running_score=0,
):
    global best_score, best_path
    if best_by_node[loc] < running_score:
        # Bail early, we've already found a more efficent path to get here.
        # TODO: Worry about orientation though - perhaps add a tolerance?
        return
    best_by_node[loc] = running_score

    if visited is None:
        visited = set()
    if running_score > best_score:
        return
    if MAP[loc] == "E" and running_score < best_score:
        print(f"Found a path! {running_score=} {best_score=}")
        best_score = running_score
        best_path = visited
        return
    elif MAP[loc] == "#":
        return
    # Set will be passed by reference, so make a copy since we're backtracking.
    visited = deepcopy(visited)
    visited.add(loc)

    for rotation in 1, -1j, 1j:
        new_orientation = orientation * rotation
        neighbor = loc + new_orientation
        if neighbor in visited:
            continue

        new_running_score = running_score + 1
        if rotation.imag:
            new_running_score += 1000
        traverse_all(neighbor, new_orientation, visited, new_running_score)


start_loc = [k for k, v in MAP.items() if v == "S"][0]

traverse_all(start_loc)
print(best_score)
