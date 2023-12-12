import collections
import enum


class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


CARD_STRENGTH = {
    "A": 13,
    "K": 12,
    "Q": 11,
    "J": 10,
    "T": 9,
    "9": 8,
    "8": 7,
    "7": 6,
    "6": 5,
    "5": 4,
    "4": 3,
    "3": 2,
    "2": 1,
}


class Hand:
    def __init__(self, hand_str, jokers=False):
        self.hand_str = hand_str
        self.cards = [CARD_STRENGTH[card] for card in hand_str]
        self.jokers = jokers
        self.type = self._get_type()

    def __repr__(self):
        return f"<Hand: {self.hand_str}>"

    def _get_freq(self):
        freq = collections.Counter(self.cards)
        if self.jokers and 0 < freq[10] < 5:
            num_jokers = freq[10]
            del freq[10]
            highest_card = sorted(
                freq.most_common(4),
                key=lambda x: (x[1], CARD_STRENGTH.get(x[0])),
                reverse=True,
            )[0][0]
            freq[highest_card] += num_jokers
        return freq

    def _get_type(self):
        freq = self._get_freq().most_common(5)
        if freq[0][1] == 5:
            return HandType.FIVE_OF_A_KIND
        if freq[0][1] == 4:
            return HandType.FOUR_OF_A_KIND
        if freq[0][1] == 3:
            if freq[1][1] == 2:
                return HandType.FULL_HOUSE
            return HandType.THREE_OF_A_KIND
        if freq[0][1] == 2:
            if freq[1][1] == 2:
                return HandType.TWO_PAIR
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        if self.jokers:
            return [0 if c == 10 else c for c in self.cards] < [
                0 if c == 10 else c for c in other.cards
            ]
        return self.cards < other.cards


def parse_input(input_str, jokers=False):
    hands = []
    for line in input_str.splitlines():
        hand_str, bid_str = line.split()
        hands.append((Hand(hand_str, jokers=jokers), int(bid_str)))
    return hands


def part_one(puzzle_input):
    hands = parse_input(puzzle_input)
    result = 0
    for i, hand in enumerate(sorted(hands), start=1):
        result += i * hand[1]
    return result


def part_two(puzzle_input):
    hands = parse_input(puzzle_input, jokers=True)
    result = 0
    for i, hand in enumerate(sorted(hands), start=1):
        print(i, hand)
        result += i * hand[1]
    return result
