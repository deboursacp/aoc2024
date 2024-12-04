# with open("example_input.txt") as f:
with open("part1_input.txt") as f:
    reports = f.readlines()


def is_safe(report: list) -> bool:
    d_level = [n2 - n1 for n2, n1 in zip(report[1:], report)]
    # Test monotonic
    if not (all((d > 0 for d in d_level)) or all((d < 0 for d in d_level))):
        return False
    # Test 0 < magnitude <= 3
    if not all(0 < abs(d) <= 3 for d in d_level):
        return False
    return True


def is_safe_with_dampner(report: str) -> bool:
    report = list(map(int, report.strip().split(" ")))
    if is_safe(report):
        return True
    # Test if the report would be safe by dropping an element.
    for i in range(len(report)):
        damped_report = report[:i] + report[i + 1 :]
        if is_safe(damped_report):
            return True
    return False


report_safety = [is_safe_with_dampner(report) for report in reports]
print(sum(report_safety))
