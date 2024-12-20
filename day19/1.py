towels, designs = open("in.txt").read().split("\n\n")
towels = towels.split(", ")
designs = designs.splitlines()


def is_possible(design: str, towels: list[str]) -> bool:
    for towel in towels:
        if towel == design:
            return True
        if design.startswith(towel):
            maybe_is_possible = is_possible(design[len(towel) :], towels)
            if maybe_is_possible:
                return True
    return False


sum([is_possible(design, towels) for design in designs])
