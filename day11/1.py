NUM_BLINKS = 25
with open("in.txt") as f:
    stones = list(map(int, f.readline().split()))
stones


def update_stone(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        s = str(stone)
        return [int(s[: len(s) // 2]), int(s[len(s) // 2 :])]
    return [stone * 2024]


for i in range(NUM_BLINKS):
    print(i)
    stones = sum([update_stone(s) for s in stones], [])
print(len(stones))
