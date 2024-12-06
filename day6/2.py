import copy

with open("in.txt") as f:
    raw_map = f.read().splitlines()
MAP = {i: {j: c for j, c in enumerate(row)} for i, row in enumerate(raw_map)}
STARTING_POSITION = [
    (outer_key, inner_key)
    for outer_key, inner_dict in MAP.items()
    for inner_key, value in inner_dict.items()
    if value == "^"
][0]


def gen_direction():
    # Since we always turn right, just iterate through a list.
    # Using a generator in a loop feels more elegant than incrementing an index modulo length
    while True:
        yield from [(-1, 0), (0, 1), (1, 0), (0, -1)]


def is_infinite_path(
    position: tuple[int, int], map: dict[int, dict[int, str]]
) -> set[tuple[int, int]]:
    # Insight: if we've already stood in the same square and orientation, we're in a loop.
    direction_generator = gen_direction()
    direction = next(direction_generator)
    visited = set()
    while True:
        if (position, direction) in visited:
            return True
        next_position = tuple(x + y for x, y in zip(position, direction))
        # Use x as the sentinel for something being out of bounds.
        next_position_value = map.get(next_position[0], {}).get(next_position[1], "x")
        if next_position_value == "x":
            # Left the grid
            return False
        elif next_position_value == "#":
            # Obstacle, so turn right
            direction = next(direction_generator)
        else:
            # Step into it and mark it visited
            visited.add((position, direction))
            position = next_position


num_looped = 0
for i in MAP.keys():
    print(f"Processing row {i} of {len(MAP.keys())}")
    for j in MAP[i].keys():
        modified_map = copy.deepcopy(MAP)
        modified_map[i][j] = "#"
        num_looped += is_infinite_path(STARTING_POSITION, modified_map)
print(num_looped)

# Insight i missed to avoid brute forcing:
# Instead of putting an obstacle in each location, you only need to put one on each location of the original path.
# Though, this would maybe cut the complexity down to 1/4th (~4k positions instead of ~16k)
