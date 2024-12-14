#!/usr/bin/env python3

"""
Advent of Code 2024-13
"""

import argparse
from math import gcd, ceil, floor
from dataclasses import dataclass

A_COST = 3
B_COST = 1

@dataclass
class Offsets:
    x: int
    y: int

@dataclass
class Machine:
    a: Offsets
    b: Offsets
    prize: Offsets

def new_empty_machine(machines):
    machine = Machine(Offsets(0, 0), Offsets(0, 0), Offsets(0, 0))
    machines.append(machine)
    return machine

def update_machine(machine, line_type, x, y):
    scale_factor = 0
    if line_type == "Button A":
        offset = machine.a
    elif line_type == "Button B":
        offset = machine.b
    elif line_type == "Prize":
        offset = machine.prize
        scale_factor = 10000000000000
    else:
        raise ValueError(f"Invalid line type: {line_type}")

    offset.x = int(x.strip()[2:]) + scale_factor
    offset.y = int(y.strip()[2:]) + scale_factor

def calc_required_tokens(machine):
    # system of equations:
    # A1 * x + B1 * y = P1
    # A2 * x + B2 * y = P2
    # solve for y:
    # y = (P1 * A2 - P2 * A1) / (B1 * A2 - A1 * B2)
    # solve for x:
    # x = (P1 - B1 * y) / A1

    # pylint: disable=invalid-name
    A1 = machine.a.x
    B1 = machine.b.x
    P1 = machine.prize.x
    A2 = machine.a.y
    B2 = machine.b.y
    P2 = machine.prize.y

    y = (P1 * A2 - P2 * A1) / (B1 * A2 - A1 * B2)
    if floor(y) == y:
        x = (P1 - B1 * y) / A1
        if floor(x) == x:
            return int(x * A_COST + y * B_COST)

    return 0

def main(inputfile):
    machines = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        current_machine = new_empty_machine(machines)
        for line in file:
            line = line.strip()
            if line == "":
                current_machine = new_empty_machine(machines)
                continue

            line_type, vals = line.split(":")
            x, y = vals.split(",")
            update_machine(current_machine, line_type, x, y)

    tokens = 0
    for machine in machines:
        tokens += calc_required_tokens(machine)

    print(tokens)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-13")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
