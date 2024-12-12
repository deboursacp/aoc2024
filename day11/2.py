NUM_BLINKS = 75
with open("in.txt") as f:
    stones = list(map(int, f.readline().split()))

import functools


@functools.cache
def stone_length(stone, remaining_depth) -> int:
    if remaining_depth == 0:
        return 1
    remaining_depth -= 1
    if stone == 0:
        return stone_length(1, remaining_depth)
    if len(str(stone)) % 2 == 0:
        s = str(stone)
        return stone_length(int(s[: len(s) // 2]), remaining_depth) + stone_length(
            int(s[len(s) // 2 :]), remaining_depth
        )
    return stone_length(stone * 2024, remaining_depth)


print(sum(stone_length(s, NUM_BLINKS) for s in stones))
