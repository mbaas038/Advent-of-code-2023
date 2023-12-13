import itertools
import math
import re


def step(commands):
    i = 0
    while True:
        command = commands[i % len(commands)]
        yield 1 if command == "R" else 0
        i += 1


def parse_input(input_str):
    commands, network_lines = input_str.split("\n\n")
    network = {}
    for line in network_lines.splitlines():
        groups = re.match(r"([A-Z]+) = \((.+)\)", line).groups()
        network[groups[0]] = groups[1].split(", ")
    return commands, network


def part_one(puzzle_input):
    commands, network = parse_input(puzzle_input)
    num_steps = 0
    stepper = step(commands)
    current = "AAA"
    goal = "ZZZ"
    while current != goal:
        current = network[current][next(stepper)]
        num_steps += 1

    return num_steps


def part_two(puzzle_input):
    commands, network = parse_input(puzzle_input)

    # calculate number of steps for all start nodes to reach a node ending in Z
    nodes = [node for node in network if node.endswith("A")]
    step_numbers = []
    for node in nodes:
        stepper = step(commands)
        num_steps = 0
        while not node.endswith("Z"):
            node = network[node][next(stepper)]
            num_steps += 1
        step_numbers.append(num_steps)

    # get the least common multiple
    return math.lcm(*step_numbers)
