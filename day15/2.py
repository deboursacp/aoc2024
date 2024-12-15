import re
import copy

grid, moves = open("in.txt").read().split("\n\n")

grid = re.sub("#", "##", grid)
grid = re.sub("O", "[]", grid)
grid = re.sub("\.", "..", grid)
grid = re.sub("@", "@.", grid)

DIR_MAPPING = {"<": -1j, "^": -1, ">": 1j, "v": 1}

map = {
    complex(i, j): val
    for i, r in enumerate(grid.splitlines())
    for j, val in enumerate(r.strip())
}


def print_map(map: dict[complex, str]):
    rows = int(max(i.real for i in map.keys()))
    cols = int(max(i.imag for i in map.keys()))
    grid = [[""] * (cols + 1) for _ in range(rows + 1)]
    for loc, val in map.items():
        grid[int(loc.real)][int(loc.imag)] = val
    print("\n".join("".join(v for v in r) for r in grid), "\n")


def move_robot_hor(map: dict[complex, str], dir):
    robot_loc = [k for k, v in map.items() if v == "@"][0]
    # First, acumulate load til we're at a wall
    head = robot_loc
    load = [head]
    while map[head + dir] in "[]":
        head = head + dir
        load.append(head)
    if map[head + dir] == "#":
        # The load is up against a wall, we can't move
        return map
    # Move all blocks in the direction
    # For simplicity, do it in reverse.
    for b in reversed(load):
        map[b + dir] = map[b]
    map[robot_loc] = "."
    return map


def move_robot_vert(map: dict[complex, str], dir):
    robot_loc = [k for k, v in map.items() if v == "@"][0]
    head = [robot_loc]
    load = []

    while head:
        x = head.pop(0)
        load.append(x)
        behind = x + dir
        if map[behind] == "#":
            return map
        if map[behind] == "[":
            # Don't duplicately add
            if behind not in load:
                head.append(behind)
            if behind + 1j not in load:
                head.append(behind + 1j)
        elif map[behind] == "]":
            # Don't duplicately add
            if behind not in load:
                head.append(behind)
            if behind - 1j not in load:
                head.append(behind - 1j)
    new_map = copy.deepcopy(map)
    for b in reversed(load):
        new_map[b + dir] = map[b]
        new_map[b] = "."
    return new_map


# print("Initial state")
# print_map(map)

for move in moves.replace("\n", ""):
    dir = DIR_MAPPING[move]
    if move in ("<>"):
        map = move_robot_hor(map, dir)
    else:
        map = move_robot_vert(map, dir)
    # print("Move: ", move)
    # print_map(map)

print(sum(k.imag + 100 * k.real for k, v in map.items() if v == "["))
