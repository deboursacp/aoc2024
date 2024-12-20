towels, designs = open("in.txt").read().split("\n\n")
towels = tuple(towels.split(", "))
designs = designs.splitlines()

import functools


@functools.cache
def is_possible(design: str, towels: tuple[str]) -> int:
    possible_ways = 0
    for towel in towels:
        if towel == design:
            possible_ways += 1
        if design.startswith(towel):
            possible_ways += is_possible(design[len(towel) :], towels)
    return possible_ways


sum([is_possible(design, towels) for design in designs])
