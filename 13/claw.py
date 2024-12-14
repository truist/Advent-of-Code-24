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
        # scale_factor = 10000000000000
    else:
        raise ValueError(f"Invalid line type: {line_type}")

    offset.x = int(x.strip()[2:]) + scale_factor
    offset.y = int(y.strip()[2:]) + scale_factor

def extended_euclidean(a, b):
    # math clues from ChatGPT
    # code from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Recursive_algorithm_2
    if a == 0:
        return b, 0, 1

    current_gcd, x, y = extended_euclidean(b % a, a)
    return current_gcd, y - (b // a) * x, x

def calc_possible_combos(a, b, prize):
    # math clues from ChatGPT
    # code from ChatGPT

    combos = []

    current_gcd = gcd(a, b)
    # print(f"a: {a}, b: {b}, prize: {prize}, gcd: {current_gcd}")

    if prize % current_gcd != 0:
        return combos

    current_gcd, x0, y0 = extended_euclidean(a, b)
    # print(f"current_gcd: {current_gcd}, x0: {x0}, y0: {y0}")

    scale = prize // current_gcd
    x0 *= scale
    y0 *= scale

    step_x = b // current_gcd
    step_y = a // current_gcd
    # print(f"scale: {scale}, x0: {x0}, y0: {y0}, step_x: {step_x}, step_y: {step_y}")

    k_min = ceil(-x0 / step_x) if step_x > 0 else floor(-x0 / step_x)
    k_max = floor(y0 / step_y) if step_y > 0 else ceil(y0 / step_y)
    # print(f"k_min: {k_min}, k_max: {k_max}")

    if k_min > k_max: # or k_min < 0 or k_max < 0:
        return combos

    for k in range(k_min, k_max + 1):
        x = x0 + k * step_x
        y = y0 - k * step_y
        if x >= 0 and y >= 0:
            # print(f"k: {k}, x: {x}, y: {y}")
            # print(a * x + b * y, prize)
            yield(x, y)
            # combos.append((x, y))

    # print(combos)
    # return combos

def calc_required_tokens(machine):
    print(machine)
    for possible_a, possible_b in calc_possible_combos(machine.a.x, machine.b.x, machine.prize.x):
        # print(f"possible_a: {possible_a}, possible_b: {possible_b}")
        if possible_a * machine.a.y + possible_b * machine.b.y == machine.prize.y:
            print(possible_a, possible_b)
            return possible_a * A_COST + possible_b * B_COST

    # possible_x = calc_possible_combos(machine.a.x, machine.b.x, machine.prize.x)
    # possible_y = calc_possible_combos(machine.a.y, machine.b.y, machine.prize.y)
    # intersection = [combo for combo in possible_x if combo in possible_y]
    # if len(intersection) > 0:
    #     combo = intersection[0]
    #     return combo[0] * A_COST + combo[1] * B_COST

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
