import re
from typing import Literal, NamedTuple


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, input_str):
        return cls(*map(int, re.findall(r"\d+", input_str)))

    def total_rating(self):
        return self.x + self.m + self.a + self.s


class Condition(NamedTuple):
    category: str
    operator: str
    value: int

    def check(self, part):
        if self.operator == ">":
            return getattr(part, self.category) > self.value
        return getattr(part, self.category) < self.value

    @property
    def inverted_operator(self):
        return "<=" if self.operator == ">" else ">="


class Rule(NamedTuple):
    condition: Condition | None
    target: str

    @classmethod
    def from_string(cls, input_str):
        cat, op, val_str, trg = re.match(
            r"(([xmas])([><])(\d+):)?([RAa-z]+)", input_str
        ).groups()[1:]
        return (
            cls(None, trg)
            if cat is None
            else cls(Condition(cat, op, int(val_str)), trg)
        )


def parse_input(input_str):
    splitted = input_str.split("\n\n")
    workflows = {}
    for line in splitted[0].splitlines():
        name, rule_str = line.rstrip("}").split("{")
        workflows[name] = [Rule.from_string(rule) for rule in rule_str.split(",")]

    parts = [Part.from_string(line) for line in splitted[1].splitlines()]
    return workflows, parts


def range_after_condition(condition, lo, hi, inverted=False):
    op = condition.inverted_operator if inverted else condition.operator
    if op == ">":
        lo = max(lo, condition.value + 1)
    elif op == ">=":
        lo = max(lo, condition.value)
    elif op == "<":
        hi = min(hi, condition.value - 1)
    else:
        hi = min(hi, condition.value)
    return lo, hi


def calc_ranges_after_condition(
    condition, xl, xh, ml, mh, al, ah, sl, sh, inverted=False
):
    if condition.category == "x":
        xl, xh = range_after_condition(condition, xl, xh, inverted)
    elif condition.category == "m":
        ml, mh = range_after_condition(condition, ml, mh, inverted)
    elif condition.category == "a":
        al, ah = range_after_condition(condition, al, ah, inverted)
    elif condition.category == "s":
        sl, sh = range_after_condition(condition, sl, sh, inverted)
    return xl, xh, ml, mh, al, ah, sl, sh


def part_one(puzzle_input):
    workflows, parts = parse_input(puzzle_input)
    result = 0
    for part in parts:
        current_workflow = "in"
        while current_workflow not in "RA":
            for rule in workflows[current_workflow]:
                if rule.condition and not rule.condition.check(part):
                    continue
                if rule.target in "RA":
                    if rule.target == "A":
                        result += part.total_rating()
                current_workflow = rule.target
                break
    return result


def part_two(puzzle_input):
    workflows, parts = parse_input(puzzle_input)
    result = 0
    queue = [("in", 1, 4000, 1, 4000, 1, 4000, 1, 4000)]
    while queue:
        wf, xl, xh, ml, mh, al, ah, sl, sh = queue.pop(0)
        if wf in "RA":
            if wf == "A":
                result += (xh - xl + 1) * (mh - ml + 1) * (ah - al + 1) * (sh - sl + 1)
            continue

        for rule in workflows[wf]:
            if rule.condition is not None:
                queue.append(
                    (
                        rule.target,
                        *calc_ranges_after_condition(
                            rule.condition, xl, xh, ml, mh, al, ah, sl, sh
                        ),
                    )
                )
                xl, xh, ml, mh, al, ah, sl, sh = calc_ranges_after_condition(
                    rule.condition, xl, xh, ml, mh, al, ah, sl, sh, inverted=True
                )
            else:
                queue.append((rule.target, xl, xh, ml, mh, al, ah, sl, sh))
                break
    return result
