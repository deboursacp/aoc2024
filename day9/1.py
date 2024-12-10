with open("in.txt") as f:
    disk_map = list(map(int, f.read()))
# Trick: sum(l_l, []) will flatten a list of lists.
disk = sum(
    [
        val * ((not i % 2) * [i // 2] or (i % 2) * ["."])
        for i, val in enumerate(disk_map)
    ],
    [],
)


l, r = 0, len(disk) - 1
while l < r:
    if disk[l] != ".":
        l += 1
        continue
    if disk[r] == ".":
        r -= 1
        continue
    disk[l], disk[r] = disk[r], disk[l]

sum(pos * int(id) for pos, id in enumerate(disk) if id != ".")
