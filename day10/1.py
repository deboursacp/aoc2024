MAP = {
    complex(i, j): int(val)
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}
DIRECTIONS = [1, -1, 1j, -1j]


def flatten(iter_sets):
    res = set()
    for s in iter_sets:
        res.update(s)
    return res


def _score(location: complex, altitude=0) -> set[complex]:
    "Counts the number of good hiking trails"
    if altitude == 9:
        return {location}
    # There is probably a more idomatic way to take the union of sets...
    return flatten(
        _score(location + d, altitude + 1)
        for d in DIRECTIONS
        if MAP.get(location + d, -1) == altitude + 1
    )


def score(loc):
    return len(_score(loc, 0))


print(sum(map(score, [trailhead for trailhead, val in MAP.items() if val == 0])))
