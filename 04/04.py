import re


CARD_REGEX = r"Card +\d+: ([\d ]+) \| ([\d ]+)"


def _parse_card(card):
    return [
        set(map(int, group.split())) for group in re.match(CARD_REGEX, card).groups()
    ]


def _get_points_on_card(winning_numbers, card_numbers):
    numbers = _get_winning_numbers(card_numbers, winning_numbers)
    return 2 ** (numbers - 1) if numbers else 0


def _get_winning_numbers(card_numbers, winning_numbers):
    return len(winning_numbers & card_numbers)


def _get_points_of_all_copies(points_dict, card_number):
    result = points_dict[card_number]
    for i in range(card_number + 1, card_number + 1 + points_dict[card_number]):
        if i not in points_dict:
            continue
        result += _get_points_of_all_copies(points_dict, i)
    return result


def part_one(puzzle_input):
    result = 0
    for line in puzzle_input.splitlines():
        winning_numbers, card_numbers = _parse_card(line)
        result += _get_points_on_card(winning_numbers, card_numbers)
    return result


def part_two(puzzle_input):
    points_per_card = {
        i: _get_winning_numbers(*_parse_card(line))
        for i, line in enumerate(puzzle_input.splitlines(), start=1)
    }
    result = 0
    for card_number, points in list(points_per_card.items()):
        result += 1 + _get_points_of_all_copies(points_per_card, card_number)
    return result
