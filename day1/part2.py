from collections import defaultdict

ls, rs = defaultdict(int), defaultdict(int)
with open("part1_input.txt") as f:
    for line in f.readlines():
        l, r = map(int, line.strip().split("   "))
        ls[l] += 1
        rs[r] += 1

similarity = sum(ls[k] * rs[k] * k for k, v in ls.items())
print(similarity)
