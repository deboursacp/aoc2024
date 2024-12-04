# with open('example_input.txt') as f:
with open("part1_input.txt") as f:
    lines = f.readlines()
ls, rs = [], []
for line in lines:
    l, r = map(int, line.strip().split("   "))
    ls.append(l)
    rs.append(r)

ls.sort()
rs.sort()

distance = sum((abs(a - b) for a, b in zip(ls, rs)))
print(distance)
