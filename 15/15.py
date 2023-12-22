import collections
import re


def parse_input(input_str):
    return input_str.split(",")


def hash_map(input_str):
    current_value = 0
    for char in input_str:
        current_value = ((current_value + ord(char)) * 17) % 256
    return current_value


def part_one(puzzle_input):
    init_seq = parse_input(puzzle_input)
    return sum(map(hash_map, init_seq))


def part_two(puzzle_input):
    init_seq = parse_input(puzzle_input)
    boxes = collections.defaultdict(dict)
    for step in init_seq:
        label, operation, focal_length_str = re.match(
            r"([a-z]+)([=-])(\d?)", step
        ).groups()
        box = hash_map(label)
        if operation == "-" and label in boxes[box]:
            del boxes[box][label]
        elif operation == "=":
            boxes[box][label] = int(focal_length_str)

    return sum(
        (box + 1) * i * boxes[box][lens]
        for box in boxes
        for i, lens in enumerate(boxes[box], start=1)
    )
