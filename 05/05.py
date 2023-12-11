import re


def _parse_seeds_and_map(inp):
    parts = inp.split("\n\n")
    seeds = list(map(int, re.findall(r"\d+", parts[0])))
    ranges = []
    for map_part in parts[1:]:
        map_part_lines = map_part.splitlines()
        rng = [
            list(map(int, map_part_line.split()))
            for map_part_line in map_part_lines[1:]
        ]
        ranges.append(rng)
    return seeds, ranges


def _parse_seeds_and_reversed_map(inp):
    parts = inp.split("\n\n")
    seeds = list(map(int, re.findall(r"\d+", parts[0])))
    maps = {}
    for map_part in parts[1:]:
        map_part_lines = map_part.splitlines()
        source, destination = re.match(
            r"([a-z]+)-to-([a-z]+) map:", map_part_lines[0]
        ).groups()[::-1]
        ranges = [
            list(map(int, map_part_line.split()))
            for map_part_line in map_part_lines[1:]
        ]
        maps[source] = {"destination": destination, "ranges": ranges}
    return seeds, maps


def map_src_to_dest(maps, value):
    for m in maps:
        for dest, src, rng in m:
            if src <= value < src + rng:
                value = dest + (value - src)
                break
    return value


def map_dest_to_src(maps, value):
    for m in maps:
        for src, dest, rng in m:
            if src <= value < src + rng:
                value = dest + (value - src)
                break
    return value


def part_one(puzzle_input):
    seeds, maps = _parse_seeds_and_map(puzzle_input)
    return min(map_src_to_dest(maps, seed) for seed in seeds)


def part_two(puzzle_input):
    seeds, maps = _parse_seeds_and_map(puzzle_input)
    maps.reverse()
    result = 0
    while True:
        result += 1
        src = map_dest_to_src(maps, result)

        for i in range(0, len(seeds), 2):
            if seeds[i] <= src < seeds[i] + seeds[i + 1]:
                return result
