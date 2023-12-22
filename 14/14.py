def parse_input(input_str):
    rounded = []
    cubes = set()
    for i, line in enumerate(input_str.splitlines()):
        for j, char in enumerate(line):
            if char == "#":
                cubes.add((i, j))
            elif char == "O":
                rounded.append((i, j))
    return rounded, cubes


def slide_rocks(rounded, cubes):
    moved = []
    rounded.sort()
    for y, x in rounded:
        while y > 0:
            new_y = y - 1
            if (new_y, x) in moved or (new_y, x) in cubes:
                break
            y = new_y
        moved.append((y, x))
    return moved


def rotate_coord_clockwise(point, grid_size):
    y, x = point
    new_y = x
    new_x = grid_size - 1 - y
    return new_y, new_x


def calculate_load(grid_size, moved):
    result = 0
    for y, x in moved:
        result += grid_size - y
    return result


def part_one(puzzle_input):
    rounded, cubes = parse_input(puzzle_input)
    moved = slide_rocks(rounded, cubes)
    return calculate_load(len(puzzle_input.splitlines()), moved)


def part_two(puzzle_input):
    moved, cubes = parse_input(puzzle_input)
    grid_size = len(puzzle_input.splitlines())

    states = {}
    target = 1_000_000_000
    i = 0

    while i < target:
        i += 1
        for _ in range(4):
            moved = [
                rotate_coord_clockwise(rock, grid_size)
                for rock in slide_rocks(moved, cubes)
            ]
            cubes = {rotate_coord_clockwise(rock, grid_size) for rock in cubes}
        moved_tuple = tuple(moved)
        if moved_tuple in states:
            cycle_length = i - states[moved_tuple]
            amt = (target - i) // cycle_length
            i += amt * cycle_length
        states[moved_tuple] = i

    return calculate_load(grid_size, moved)
