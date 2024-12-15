grid, moves = open("in.txt").read().split("\n\n")

DIR_MAPPING = {"<": -1j, "^": -1, ">": 1j, "v": 1}

MAP = {
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


def move_robot(map: dict[complex, str], dir):
    robot_loc = [k for k, v in map.items() if v == "@"][0]
    # First, acumulate load til we're at a wall
    head = robot_loc
    load = [head]
    while MAP[head + dir] == "O":
        head = head + dir
        load.append(head)
    if MAP[head + dir] == "#":
        # The load is up against a wall, we can't move
        return
    elif MAP[head + dir] == ".":
        # Move all blocks in the direction
        # For simplicity, do it in reverse.
        for b in reversed(load):
            MAP[b + dir] = MAP[b]
        MAP[robot_loc] = "."
    else:
        raise RuntimeError("Load should end at empty space or wall.")


# print("Initial state")
# print_map(MAP)

for move in moves.replace("\n", ""):
    dir = DIR_MAPPING[move]
    move_robot(MAP, dir)
    # print("Move: ", move)
    # print_map(MAP)

print(sum(k.imag + 100 * k.real for k, v in MAP.items() if v == "O"))
