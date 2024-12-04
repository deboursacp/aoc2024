with open("day4/in.txt") as f:
    PUZ = f.read().splitlines()

NEEDLE = "XMAS"
X_MAX = len(PUZ) - 1
Y_MAX = len(PUZ[0]) - 1


def directions():
    for x in -1, 0, 1:
        for y in -1, 0, 1:
            if x == y == 0:
                continue
            yield x, y


def is_out_of_bounds(x, y):
    return not (0 <= x <= X_MAX and 0 <= y <= Y_MAX)


def is_match(x_start, y_start, dir):
    for i, letter in enumerate(NEEDLE):
        x, y = x_start + i * dir[0], y_start + i * dir[1]
        if is_out_of_bounds(x, y) or PUZ[x][y] != letter:
            return False
    return True


matches = 0
for x, row in enumerate(PUZ):
    for y in range(len(row)):
        for dir in directions():
            matches += is_match(x, y, dir)
print(matches)
