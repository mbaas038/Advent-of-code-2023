import math
from typing import Self


LOW = False
HIGH = True


class Module:
    def __init__(self, name) -> None:
        self.name = name
        self.destination_modules = []

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"

    def receive_pulse(self, sender: Self, pulse: bool) -> list[tuple[Self, Self, bool]]:
        return []

    def add_destination_modules(self, modules: list[Self]) -> None:
        self.destination_modules.extend(modules)


class FlipFlopModule(Module):
    enabled = False

    def receive_pulse(
        self, sender: Module, pulse: bool
    ) -> list[tuple[Module, Module, bool]]:
        if pulse:
            return []
        new_pulses = [
            (self, destination_module, not self.enabled)
            for destination_module in self.destination_modules
        ]
        self.flip_switch()
        return new_pulses

    def flip_switch(self) -> None:
        self.enabled = not self.enabled


class ConjunctionModule(Module):
    def __init__(self, name) -> None:
        super().__init__(name)
        self.input_pulses = {}

    def receive_pulse(
        self, sender: Module, pulse: bool
    ) -> list[tuple[Module, Module, bool]]:
        self.input_pulses[sender] = pulse
        return [
            (self, destination_module, not all(self.input_pulses.values()))
            for destination_module in self.destination_modules
        ]


class BroadcastModule(Module):
    def receive_pulse(
        self, sender: Module, pulse: bool
    ) -> list[tuple[Module, Module, bool]]:
        return [
            (self, destination_module, pulse)
            for destination_module in self.destination_modules
        ]


def parse_input(input_str: str) -> dict[str, Module]:
    lines = input_str.splitlines()
    modules = {}
    for line in lines:
        name = line.split(" -> ")[0]
        if name == "broadcaster":
            modules[name] = BroadcastModule(name)
        elif name[0] == "%":
            modules[name[1:]] = FlipFlopModule(name[1:])
        elif name[0] == "&":
            modules[name[1:]] = ConjunctionModule(name[1:])
        else:
            raise AssertionError(f"Unknown module: {name}")

    for line in lines:
        name, receivers_str = line.lstrip("%&").split(" -> ")
        receivers = []
        for receiver in receivers_str.split(", "):
            module = modules.get(receiver, Module(receiver))
            if isinstance(module, ConjunctionModule):
                module.input_pulses[modules[name]] = False
            receivers.append(module)
        modules[name].add_destination_modules(receivers)

    return modules


def part_one(puzzle_input):
    modules = parse_input(puzzle_input)
    low = 0
    high = 0
    for _ in range(1000):
        signals = modules["broadcaster"].receive_pulse(Module("button"), LOW)
        lo = 1
        hi = 0
        while signals:
            sender, destination, pulse = signals.pop(0)
            if pulse == LOW:
                lo += 1
            else:
                hi += 1
            signals.extend(destination.receive_pulse(sender, pulse))
        low += lo
        high += hi
    return low * high


def part_two(puzzle_input):
    modules = parse_input(puzzle_input)
    dest_module = [
        module
        for module in modules.values()
        if "rx" in (dest_m.name for dest_m in module.destination_modules)
    ][0]
    input_modules = {
        module: None
        for module in modules.values()
        if dest_module in module.destination_modules
    }
    button_presses = 0
    while any(val is None for val in input_modules.values()):
        signals = modules["broadcaster"].receive_pulse(Module("button"), LOW)
        button_presses += 1
        while signals:
            sender, destination, pulse = signals.pop(0)
            if (
                sender in input_modules
                and pulse == HIGH
                and input_modules[sender] is None
            ):
                input_modules[sender] = button_presses

            signals.extend(destination.receive_pulse(sender, pulse))

    return math.lcm(*input_modules.values())
