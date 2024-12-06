import re

MUL_REGEX_PATTERN = r"(mul\(\d{1,3},\d{1,3}\))|(do\(\))|(don't\(\))"

with open("in.txt") as f:
    lines = f.readlines()
# lines = ["xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"]


def compute_matched_mul(match: str) -> int:
    l, r = map(int, match[4:-1].split(","))
    return l * r


total = 0
enabled = True
for line in lines:
    matches = re.findall(MUL_REGEX_PATTERN, line)
    for mul, do, dont in matches:
        if do:
            enabled = True
        elif dont:
            enabled = False
        else:
            if enabled:
                total += compute_matched_mul(mul)
print(total)
