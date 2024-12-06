import re

MUL_REGEX_PATTERN = "(mul\(\d{1,3},\d{1,3}\))"

with open("in.txt") as f:
    lines = f.readlines()


def compute_matched_mul(match: str) -> int:
    l, r = map(int, match[4:-1].split(","))
    return l * r


total = 0
for line in lines:
    matches = re.findall(MUL_REGEX_PATTERN, line)
    total += sum(compute_matched_mul(match) for match in matches)
print(total)
