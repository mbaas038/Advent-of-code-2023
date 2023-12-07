import math
import re


PATTERN = r"(\d+) (red|green|blue)"

MAX_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def part_one(puzzle_input):
    result = 0
    for game_id, game in enumerate(puzzle_input.split("\n"), start=1):
        possible = True
        for no_of_cubes, color in re.findall(PATTERN, game):
            if int(no_of_cubes) > MAX_CUBES[color]:
                possible = False
                break
        if possible:
            result += int(game_id)
    return result


def part_two(puzzle_input):
    result = 0
    for game in puzzle_input.split("\n"):
        maxes = {color: 0 for color in MAX_CUBES.keys()}
        for no_of_cubes, color in re.findall(PATTERN, game):
            maxes[color] = max(int(no_of_cubes), maxes[color])
        result += math.prod(maxes.values())
    return result
