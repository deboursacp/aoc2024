with open("in.txt") as f:
    raw_map = f.read().splitlines()


def gen_direction():
    # Since we always turn right, just iterate through a list.
    # Using a generator in a loop feels more elegant than incrementing an index modulo length
    while True:
        yield from [(-1, 0), (0, 1), (1, 0), (0, -1)]


# 'x' is our sentinel for stepping out of bounds.
bounded_map = [
    "x" * (len(raw_map[0]) + 2),
    *["x" + r + "x" for r in raw_map],
    "x" * (len(raw_map[0]) + 2),
]
guard_pos = [(i, r.index("^")) for i, r in enumerate(bounded_map) if "^" in r][0]


def walk_guard_path(
    position: tuple[int, int], bounded_map: list[str]
) -> set[tuple[int, int]]:
    visited = {position}
    direction_generator = gen_direction()
    direction = next(direction_generator)
    while True:
        next_position = (position[0] + direction[0], position[1] + direction[1])
        next_position_value = bounded_map[next_position[0]][next_position[1]]
        if next_position_value == "x":
            # Left the grid
            return visited
        elif next_position_value == "#":
            # Obstacle, so turn right
            direction = next(direction_generator)
        else:
            # Step into it and mark it visited
            position = next_position
            visited.add(position)


visited = walk_guard_path(guard_pos, bounded_map)
print(len(visited))
