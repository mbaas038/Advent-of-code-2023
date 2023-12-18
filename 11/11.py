import itertools


def solve(input_str, factor=2):
    rows = input_str.splitlines()
    galaxies = [
        [i, j]
        for i, line in enumerate(rows)
        for j, char in enumerate(line)
        if char == "#"
    ]
    blank_rows = [i for i, line in enumerate(rows) if set(line) == {"."}]
    blank_cols = [i for i, line in enumerate(zip(*rows)) if set(line) == {"."}]

    # expand
    for galaxy in galaxies:
        galaxy[0] += sum(i < galaxy[0] for i in blank_rows) * (factor - 1)
        galaxy[1] += sum(i < galaxy[1] for i in blank_cols) * (factor - 1)

    return sum(
        abs(x[0] - y[0]) + abs(x[1] - y[1])
        for x, y in itertools.combinations(galaxies, 2)
    )


def part_one(puzzle_input):
    return solve(puzzle_input)


def part_two(puzzle_input):
    return solve(puzzle_input, factor=1_000_000)
