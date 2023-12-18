import enum


class DIRECTION(enum.Enum):
    EAST = (0, 1)
    WEST = (0, -1)
    NORTH = (-1, 0)
    SOUTH = (1, 0)


PIPE_PARTS = {
    "|": {DIRECTION.NORTH: DIRECTION.NORTH, DIRECTION.SOUTH: DIRECTION.SOUTH},
    "-": {DIRECTION.WEST: DIRECTION.WEST, DIRECTION.EAST: DIRECTION.EAST},
    "L": {
        DIRECTION.SOUTH: DIRECTION.EAST,
        DIRECTION.WEST: DIRECTION.NORTH,
    },
    "J": {
        DIRECTION.SOUTH: DIRECTION.WEST,
        DIRECTION.EAST: DIRECTION.NORTH,
    },
    "7": {
        DIRECTION.NORTH: DIRECTION.WEST,
        DIRECTION.EAST: DIRECTION.SOUTH,
    },
    "F": {
        DIRECTION.NORTH: DIRECTION.EAST,
        DIRECTION.WEST: DIRECTION.SOUTH,
    },
}


def find_starting_point(grid):
    for i, row in enumerate(grid):
        if "S" in row:
            return i, row.find("S")


def get_start_directions(grid, starting_point):
    directions = []
    for d in DIRECTION:
        dy, dx = d.value
        neighbour_y = starting_point[0] + dy
        if 0 <= neighbour_y < len(grid):
            neighbour_x = starting_point[1] + dx
            if 0 <= neighbour_x < len(grid[starting_point[0]]):
                if grid[neighbour_y][neighbour_x] in PIPE_PARTS:
                    if d in PIPE_PARTS[grid[neighbour_y][neighbour_x]]:
                        directions.append(d)
    return directions


def move(grid, direction, y, x):
    dy, dx = direction.value
    new_y, new_x = y + dy, x + dx
    new_direction = direction
    if grid[new_y][new_x] in PIPE_PARTS:
        new_direction = PIPE_PARTS[grid[new_y][new_x]][direction]
    return new_y, new_x, new_direction


def part_one(puzzle_input):
    grid = puzzle_input.splitlines()

    current_tile = starting_point = find_starting_point(grid)
    direction = get_start_directions(grid, starting_point)[0]

    num_pipe_parts = 0
    while not num_pipe_parts or current_tile != starting_point:
        num_pipe_parts += 1
        new_y, new_x, direction = move(grid, direction, *current_tile)
        current_tile = new_y, new_x

    return num_pipe_parts // 2


def part_two(puzzle_input):
    grid = puzzle_input.splitlines()
    loop_grid = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    current_tile = starting_point = find_starting_point(grid)
    loop_grid[starting_point[0]][starting_point[1]] = 1
    start_directions = get_start_directions(grid, starting_point)
    direction = start_directions[0]

    num_pipe_parts = 0
    while not num_pipe_parts or current_tile != starting_point:
        num_pipe_parts += 1
        new_y, new_x, direction = move(grid, direction, *current_tile)
        loop_grid[new_y][new_x] = 1
        current_tile = new_y, new_x

    result = 0
    s_is_pipe = (
        DIRECTION.NORTH in start_directions or DIRECTION.SOUTH in start_directions
    )
    for i in range(len(grid)):
        in_loop = False
        for j in range(len(grid[0])):
            if loop_grid[i][j]:
                if grid[i][j] in "|F7" or (grid[i][j] == "S" and s_is_pipe):
                    in_loop = not in_loop
            elif in_loop:
                loop_grid[i][j] = "X"
                result += 1

    return result
