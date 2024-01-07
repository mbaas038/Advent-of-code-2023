from collections import deque


def parse_input(input_str: str) -> tuple[list[list[str]], tuple[int, int]]:
    grid = []
    pos = None
    for i, line in enumerate(input_str.splitlines()):
        row = []
        for j, char in enumerate(line):
            if char == "S":
                pos = i, j
                row.append(".")
            else:
                row.append(char)
        grid.append(row)
    return grid, pos


def bfs(
    grid: list[list[str]], start: tuple[int, int], steps: int, infinite: bool = False
) -> int:
    queue = deque([(start, steps)])
    visited = set()
    possible_locations = set()
    while queue:
        location, remaining_steps = queue.popleft()
        if remaining_steps >= 0:
            if remaining_steps % 2 == 0:
                possible_locations.add(location)

            if remaining_steps > 0:
                remaining_steps -= 1
                y, x = location
                for neighbour_y, neighbour_x in [
                    (y + dy, x + dx) for dy, dx in [(0, -1), (0, 1), (-1, 0), (1, 0)]
                ]:
                    if infinite:
                        ny, nx = neighbour_y % len(grid), neighbour_x % len(grid[0])
                    else:
                        ny, nx = neighbour_y, neighbour_x
                        if not (
                            0 <= neighbour_y < len(grid)
                            and 0 <= neighbour_x < len(grid[0])
                        ):
                            continue
                    if (neighbour_y, neighbour_x) in visited or grid[ny][nx] == "#":
                        continue
                    queue.append(((neighbour_y, neighbour_x), remaining_steps))
                    visited.add((neighbour_y, neighbour_x))

    return len(possible_locations)


def part_one(puzzle_input: str) -> int:
    grid, start = parse_input(puzzle_input)
    return bfs(grid, start, 64)


def part_two(puzzle_input: str) -> int:
    grid, start = parse_input(puzzle_input)
    x = (26501365 - len(grid) // 2) // len(grid)
    p1 = bfs(grid, start, start[0], infinite=True)
    p2 = bfs(grid, start, start[0] + len(grid), infinite=True)
    p3 = bfs(grid, start, start[0] + len(grid) * 2, infinite=True)
    c = p1
    b = (4 * p2 - 3 * p1 - p3) // 2
    a = p2 - p1 - b
    return a * x**2 + b * x + c
