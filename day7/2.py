import itertools

with open("in.txt") as f:
    lines = f.readlines()


def evaluate(operands: list[int], operations: list[str]) -> int:
    # Can't use eval() since we always go left to right.
    running_total = operands[0]
    for i, operand in enumerate(operands[1:]):
        if operations[i] == "*":
            running_total *= operand
        elif operations[i] == "+":
            running_total += operand
        elif operations[i] == "||":
            running_total = int(str(running_total) + str(operand))
    return running_total


tot = 0
for l in lines:
    tv, operands = l.split(":")
    operands = list(map(int, operands.split()))
    for operations in itertools.product(("*", "+", "||"), repeat=len(operands) - 1):
        if evaluate(operands, operations) == int(tv):
            tot += int(tv)
            break
print(tot)
