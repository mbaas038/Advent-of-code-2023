import argparse
import importlib
import time


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("day")
    parser.add_argument("--part-one", action='store_true')
    parser.add_argument("--part-two", action='store_true')
    return parser


if __name__ == "__main__":
    arg_parser = create_parser()

    args = arg_parser.parse_args()
    day = args.day.zfill(2)

    day_mod = importlib.import_module(f"{day}.{day}")

    puzzle_input = open(f"{day}/{day}.txt", "r").read()
    for i, puzzle in enumerate((args.part_one, args.part_two), start=1):
        if puzzle:
            print(f" Part {i} ".center(50, "-"))
            t0 = time.time()
            solve = day_mod.part_one if i == 1 else day_mod.part_two
            print("Solution:")
            print(solve(puzzle_input))
            print(f"Elapsed time: {time.time() - t0} ms")
            print(f"{50 * '-'}\n")

