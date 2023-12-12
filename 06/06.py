import math
import re


def _parse_input(input_str):
    return [list(map(int, re.findall("\d+", line))) for line in input_str.splitlines()]


def solve_quadratic(time, distance):
    discriminant = math.sqrt(time**2 - 4 * distance)

    solutions = [(-time + discriminant * mtp) / 2 for mtp in (-1, 1)]
    return len(range(math.floor(solutions[0] + 1), math.ceil(solutions[1])))


def part_one(puzzle_input):
    times, distances = _parse_input(puzzle_input)
    result = []
    for time, distance in zip(times, distances):
        result.append(solve_quadratic(-time, distance))
    return math.prod(result)


def part_two(puzzle_input):
    times, distances = _parse_input(puzzle_input)
    return solve_quadratic(
        int("".join(map(str, times))), int("".join(map(str, distances)))
    )
