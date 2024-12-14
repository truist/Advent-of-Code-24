#!/usr/bin/env python3

"""
Advent of Code 2024-13
"""

import argparse

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
    if line_type == "Button A":
        offset = machine.a
    elif line_type == "Button B":
        offset = machine.b
    elif line_type == "Prize":
        offset = machine.prize
    else:
        raise ValueError(f"Invalid line type: {line_type}")

    offset.x = int(x.strip()[2:])
    offset.y = int(y.strip()[2:])

def calc_possible_combos(a, b, prize):
    combos = []
    for i in range(0, prize, a):
        for j in range(0, prize, b):
            # print(i, j, prize, i + j)
            if i + j == prize:
                combos += [(i // a, j // b)]

    return combos

def calc_required_tokens(machine):
    possible_x = calc_possible_combos(machine.a.x, machine.b.x, machine.prize.x)
    possible_y = calc_possible_combos(machine.a.y, machine.b.y, machine.prize.y)
    intersection = [combo for combo in possible_x if combo in possible_y]
    if len(intersection) > 0:
        combo = intersection[0]
        return combo[0] * A_COST + combo[1] * B_COST

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
