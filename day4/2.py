with open("day4/in.txt") as f:
    puz = f.read().splitlines()

NEEDLE = "MAS"
X_MAX = len(puz) - 1
Y_MAX = len(puz[0]) - 1


def directions():
    for x in 1, -1:
        for y in 1, -1:
            yield x, y


def is_out_of_bounds(x, y):
    return not (0 <= x <= X_MAX and 0 <= y <= Y_MAX)


def is_match(x_start, y_start, dir):
    for i, letter in enumerate(NEEDLE):
        x, y = x_start + i * dir[0], y_start + i * dir[1]
        if is_out_of_bounds(x, y) or puz[x][y] != letter:
            return False
    return True


def is_xmas(x_center, y_center):
    matches = 0
    for dir in directions():
        # take a step backwards in the direction, then check if it's a match
        x_start, y_start = x_center - dir[0], y_center - dir[1]
        matches += is_match(x_start, y_start, dir)
    return matches == 2


matches = 0
for x, row in enumerate(puz):
    for y, center_letter in enumerate(row):
        if center_letter == "A":
            matches += is_xmas(x, y)
print(matches)
