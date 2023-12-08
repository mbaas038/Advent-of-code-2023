import math
import re


def _find_symbol_coords(grid):
    coords = set()
    for i, row in enumerate(grid):
        for j, character in enumerate(row):
            if not character.isdigit() and character != ".":
                coords.add((i, j))
    return coords


def _find_numbers(grid):
    """Return a tuple with number string, x and y coord"""
    numbers = set()
    for i, row in enumerate(grid):
        for number in re.finditer(r"\d+", row):
            numbers.add((number.group(), i, number.span()[0]))
    return numbers


def _calculate_neighbours(grid, number_length, i, j):
    """Return a set with the coords of the neighbours"""
    neighbours = set()
    for y in range(i - 1, i + 2):
        if not 0 <= y < len(grid):
            # check if y coord is on grid
            continue
        for x in range(j - 1, j + number_length + 1):
            if not 0 <= x < len(grid[0]):
                # check if x coord is on grid
                continue

            if y == i and j <= x < j + number_length:
                # check if xy coord is on the number
                continue
            neighbours.add((y, x))
    return neighbours


def _find_gears(grid):
    """Find the coords of the gears."""
    coords = set()
    for i, row in enumerate(grid):
        for j, character in enumerate(row):
            if character == "*":
                coords.add((i, j))
    return coords


def _find_number_coords(grid):
    """Get all the coords where a number is placed."""
    numbers = _find_numbers(grid)
    coord_dict = {}
    for number_string, y, x in numbers:
        number = int(number_string)
        coord_dict[
            frozenset([(y, i) for i in range(x, x + len(number_string))])
        ] = number
    return coord_dict


def _get_part_numbers_for_gear(gear_coord, grid, number_coords):
    """Get the part numbers for each gear."""
    part_numbers = []
    visited = set()
    possible_neighbours = _calculate_neighbours(grid, 1, *gear_coord)
    for neighbour in possible_neighbours:
        for number_coord_set in number_coords:
            if len({neighbour} & number_coord_set) and neighbour not in visited:
                part_numbers.append(number_coords[number_coord_set])
                visited |= number_coord_set
    return part_numbers


def part_one(puzzle_input):
    result = 0
    grid = puzzle_input.splitlines()
    symbol_coords = _find_symbol_coords(grid)
    numbers = _find_numbers(grid)
    for number_string, i, j in numbers:
        possible_neighbours = _calculate_neighbours(grid, len(number_string), i, j)
        if len(possible_neighbours & symbol_coords):
            result += int(number_string)
    return result


def part_two(puzzle_input):
    result = 0
    grid = puzzle_input.splitlines()
    gear_coords = _find_gears(grid)
    number_coords = _find_number_coords(grid)
    for gear_coord in gear_coords:
        part_numbers = _get_part_numbers_for_gear(gear_coord, grid, number_coords)
        if len(part_numbers) == 2:
            result += math.prod(part_numbers)
    return result
