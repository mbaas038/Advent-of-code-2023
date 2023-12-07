import re


def part_one(puzzle_input):
    return sum(
        int(re.search(r"\d", line).group() + re.search(r"\d", line[::-1]).group())
        for line in puzzle_input.split("\n")
    )


TEXT_TO_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part_two(puzzle_input):
    pattern = f"(?=({'|'.join(TEXT_TO_NUMBERS.keys())}|\d))"
    result = 0
    for line in puzzle_input.split("\n"):
        match = re.findall(pattern, line)
        result += int(
            TEXT_TO_NUMBERS.get(match[0], match[0])
            + TEXT_TO_NUMBERS.get(match[-1], match[-1])
        )
    return result
