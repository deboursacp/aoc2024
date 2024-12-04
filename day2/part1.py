# with open('example_input.txt') as f:
with open("part1_input.txt") as f:
    reports = f.readlines()


def is_safe(report: str) -> bool:
    report = report.strip().split(" ")
    d_level = [int(n2) - int(n1) for n2, n1 in zip(report[1:], report)]
    # Test monotonic
    if not (all((d > 0 for d in d_level)) or all((d < 0 for d in d_level))):
        return False
    # Test 0 < magnitude <= 3
    if not all(0 < abs(d) <= 3 for d in d_level):
        return False
    return True


report_safety = [is_safe(report) for report in reports]
print(sum(report_safety))
