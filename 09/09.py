

def parse_input(input_str):
    return [list(map(int, line.split())) for line in input_str.splitlines()]


def calc_next_number(sequence, prt_two=False):
    if not any(sequence):
        return 0
    if prt_two:
        sequence.reverse()
    return sequence[-1] + calc_next_number(
        [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
    )


def part_one(puzzle_input):
    sequences = parse_input(puzzle_input)
    return sum(calc_next_number(sequence) for sequence in sequences)


def part_two(puzzle_input):
    sequences = parse_input(puzzle_input)
    return sum(calc_next_number(sequence, prt_two=True) for sequence in sequences)
