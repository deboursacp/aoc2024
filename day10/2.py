MAP = {
    complex(i, j): int(val)
    for i, r in enumerate(open("ex.txt"))
    for j, val in enumerate(r.strip())
}
DIRECTIONS = [1, -1, 1j, -1j]


def flatten(iter_sets):
    res = set()
    for s in iter_sets:
        res.update(s)
    return res


def score(location: complex, altitude=0) -> int:
    "Counts the number of good hiking trails"
    # If I wanted to share the score function across part 1 & 2, I think I could do it by returning a tuple.
    if altitude == 9:
        return 1
    return sum(
        score(location + d, altitude + 1)
        for d in DIRECTIONS
        if MAP.get(location + d, -1) == altitude + 1
    )


print(sum(map(score, [trailhead for trailhead, val in MAP.items() if val == 0])))
