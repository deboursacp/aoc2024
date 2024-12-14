MAP = {
    complex(i, j): val
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}
DIRECTIONS = [1, -1, 1j, -1j]

seen: set[complex] = set()
regions: list[set[complex]] = []
for loc, crop_type in MAP.items():
    if loc in seen:
        continue
    region: set[complex] = set()
    # Do traverse the contiguous region.
    q = set([loc])
    while q:
        s = q.pop()
        seen.add(s)
        region.add(s)
        for dir in DIRECTIONS:
            next = s + dir
            if next in MAP and next not in seen and MAP[next] == crop_type:
                q.add(next)
    regions.append(region)


def calculate_cost(region: set[complex]):
    # Insight: num_fences = 4*count - # adjacent_pairs (non-deduped)
    # To count adjacent cells: instead of iterating over all pairs which would be O(n^2), iterate over neighbors O(4n)
    return len(region) * (
        4 * len(region)
        - len([p + dir for p in region for dir in DIRECTIONS if p + dir in region])
    )


print(sum([calculate_cost(r) for r in regions]))
