def parse_input(input_str):
    return [
        [list(line) for line in pattern.splitlines()]
        for pattern in input_str.split("\n\n")
    ]


def find_mirror(pattern):
    for i in range(len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            no_of_lines_besides = min(i, len(pattern) - (i + 2))
            left = pattern[i - no_of_lines_besides : i]
            right = pattern[i + 2 : i + 2 + no_of_lines_besides][::-1]
            if left == right:
                return i + 1


def find_smudged_mirror(pattern):
    for i in range(len(pattern) - 1):
        no_of_lines_besides = min(i, len(pattern) - (i + 2))
        left = pattern[i - no_of_lines_besides : i] + [pattern[i]]
        right = pattern[i + 2 : i + 2 + no_of_lines_besides][::-1] + [pattern[i + 1]]
        if sum(i != j for l, r in zip(left, right) for i, j in zip(l, r)) == 1:
            return i + 1


def part_one(puzzle_input):
    patterns = parse_input(puzzle_input)
    result = 0
    for pattern in patterns:
        # try horizontal pattern
        mirror = find_mirror(pattern)
        if mirror is None:
            # try vertical pattern
            mirror = find_mirror(list(zip(*pattern)))
            result += mirror
        else:
            result += mirror * 100

    return result


def part_two(puzzle_input):
    patterns = parse_input(puzzle_input)
    result = 0
    for pattern in patterns:
        # try horizontal pattern
        mirror = find_smudged_mirror(pattern)
        if mirror is None:
            # try vertical pattern
            mirror = find_smudged_mirror(list(zip(*pattern)))
            result += mirror
        else:
            result += mirror * 100
    return result
