import re


DIRECTION_MAP = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

DIRECTION = "RDLU"


def parse_input(input_str):
    return [
        (d, int(m), c) for d, m, c in re.findall(r"([UDLR]) (\d+) \((.+)\)", input_str)
    ]


def get_outer_coords(plan):
    curr = (0, 0)
    corners = [curr]
    perimeter = 0
    for d, m, _ in plan:
        dy, dx = DIRECTION_MAP[d]
        curr = curr[0] + m * dy, curr[1] + m * dx
        corners.append(curr)
        perimeter += m
    return corners, perimeter


def shoelace_formula(coords):
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    area = (
        abs(
            sum(
                x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(coords[:-1], coords[1:])
            )
        )
        // 2
    )

    return area


def picks_theorem(area, b):
    return area - b // 2 + 1


def part_one(puzzle_input):
    dig_plan = parse_input(puzzle_input)
    corners, perimeter = get_outer_coords(dig_plan)
    area = shoelace_formula(corners)
    interior = picks_theorem(area, perimeter)
    return interior + perimeter


def part_two(puzzle_input):
    dig_plan = parse_input(puzzle_input)

    fixed_dig_plan = []
    for d, m, c in dig_plan:
        new_d = DIRECTION[int(c[-1])]
        new_m = int(c[1:-1], 16)
        fixed_dig_plan.append((new_d, new_m, c))

    corners, perimeter = get_outer_coords(fixed_dig_plan)
    area = shoelace_formula(corners)
    interior = picks_theorem(area, perimeter)
    return interior + perimeter
