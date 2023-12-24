UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


REFLECTIONS = {
    "\\": {
        UP: LEFT,
        LEFT: UP,
        DOWN: RIGHT,
        RIGHT: DOWN,
    },
    "/": {
        UP: RIGHT,
        RIGHT: UP,
        LEFT: DOWN,
        DOWN: LEFT,
    },
}


def parse_input(input_str):
    return [list(row) for row in input_str.splitlines()]


def activate_grid(grid, start_y, start_x, direction):
    states = set()
    activated = set()
    beams = {((start_y, start_x), direction)}

    while beams:
        new_beams = set()
        for position, direction in beams:
            y, x = position
            if y < 0 or y >= len(grid) or x < 0 or x >= len(grid[0]):
                continue
            if (position, direction) in states:
                continue
            states.add((position, direction))
            activated.add((y, x))

            if grid[y][x] == "\\" or grid[y][x] == "/":
                new_direction = REFLECTIONS[grid[y][x]][direction]
            elif direction in (LEFT, RIGHT) and grid[y][x] == "|":
                new_direction = UP
                new_beams.add(((y, x), DOWN))
            elif direction in (UP, DOWN) and grid[y][x] == "-":
                new_direction = LEFT
                new_beams.add(((y, x), RIGHT))
            else:
                new_direction = direction

            y, x = y + new_direction[0], x + new_direction[1]
            new_beams.add(((y, x), new_direction))

        beams = new_beams
    return activated


def print_activated_grid(grid_size, activated):
    print(
        "\n".join(
            "".join("#" if (i, j) in activated else "." for j in range(grid_size))
            for i in range(grid_size)
        )
    )


def part_one(puzzle_input):
    grid = parse_input(puzzle_input)
    activated = activate_grid(grid, 0, 0, RIGHT)
    print_activated_grid(len(grid), activated)
    return len(activated)


def part_two(puzzle_input):
    grid = parse_input(puzzle_input)
    return max(
        *(len(activate_grid(grid, 0, i, DOWN)) for i in range(len(grid))),
        *(len(activate_grid(grid, len(grid) - 1, i, UP)) for i in range(len(grid))),
        *(len(activate_grid(grid, i, 0, RIGHT)) for i in range(len(grid))),
        *(len(activate_grid(grid, i, len(grid) - 1, LEFT)) for i in range(len(grid))),
    )
