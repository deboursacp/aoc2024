# 1) If it's a 2d-coord map, which often is the case, use a dict of complex numbers:
MAP = {
    complex(i, j): val
    for i, r in enumerate(open("in.txt"))
    for j, val in enumerate(r.strip())
}
# This also allows you to add a heading easily:
pos = complex(1, 2)
dir = complex(1, 1)
new_pos = pos + dir  # 2+3j

# Rotate clockwise 90deg by 1j
rotated = dir * -1j

# You can check if you've left the map easily by checking if your pos is in the dict
in_bounds = pos in MAP

# And positions by value using:
[p for p in MAP if MAP[p] == "needle"]
