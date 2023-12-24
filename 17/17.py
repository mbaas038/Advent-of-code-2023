import heapq

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


def parse_input(input_str):
    return [list(map(int, list(line))) for line in input_str.splitlines()]


def least_heat_loss(grid, min_straight_steps, max_straight_steps):
    queue = [(0, 0, 0, 0, 0)]
    seen = set()
    while queue:
        heat_loss, y, x, dir_y, dir_x = heapq.heappop(queue)
        if y == len(grid) - 1 and x == len(grid[0]) - 1:
            return heat_loss
        if (y, x, dir_y, dir_x) in seen:
            continue
        seen.add((y, x, dir_y, dir_x))

        for dy, dx in {UP, DOWN, LEFT, RIGHT} - {(dir_y, dir_x), (-dir_y, -dir_x)}:
            new_y, new_x, new_heat_loss = y, x, heat_loss
            for i in range(1, max_straight_steps + 1):
                new_y, new_x = new_y + dy, new_x + dx
                if 0 <= new_y < len(grid) and 0 <= new_x < len(grid[0]):
                    new_heat_loss += grid[new_y][new_x]
                    if i >= min_straight_steps:
                        heapq.heappush(queue, (new_heat_loss, new_y, new_x, dy, dx))


def part_one(puzzle_input):
    grid = parse_input(puzzle_input)
    return least_heat_loss(grid, 1, 3)


def part_two(puzzle_input):
    grid = parse_input(puzzle_input)
    return least_heat_loss(grid, 4, 10)
