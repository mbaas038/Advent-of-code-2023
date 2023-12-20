import functools


def parse_input(input_str):
    rows = []
    rules = []
    for line in input_str.splitlines():
        row, rule = line.split()
        rows.append(row)
        rules.append(tuple(map(int, rule.split(","))))
    return rows, rules


@functools.cache
def solve(row, rules):
    if not rules:
        return int("#" not in row)
    if not row:
        return int(not rules)

    result = 0

    if row[0] in ".?":
        result += solve(row[1:], rules)
    if row[0] in "#?":
        if (
            rules[0] <= len(row)
            and "." not in row[: rules[0]]
            and (rules[0] == len(row) or row[rules[0]] != "#")
        ):
            result += solve(row[rules[0] + 1 :], rules[1:])

    return result


def part_one(puzzle_input):
    spring_rows, group_rules = parse_input(puzzle_input)
    result = 0
    for i in range(len(spring_rows)):
        result += solve(spring_rows[i], group_rules[i])
    return result


def part_two(puzzle_input):
    spring_rows, group_rules = parse_input(puzzle_input)
    result = 0
    for i in range(len(spring_rows)):
        result += solve("?".join([spring_rows[i]] * 5), group_rules[i] * 5)
    return result
