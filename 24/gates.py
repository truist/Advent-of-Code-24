#!/usr/bin/env python3

"""
Advent of Code 2024-24
"""

import argparse
from dataclasses import dataclass
from itertools import combinations

@dataclass
class Gate:
    in1: str
    in2: str
    op: str
    out: str
    value: int

def generate_inputs(input_lines):
    inputs = {}
    max_x = 0
    for input_line in input_lines.split("\n"):
        name, _ = input_line.split(":")
        name = name.strip()
        if name.startswith("x"):
            inputs[name] = 0
            max_x = max(max_x, int(name[1:3]))
        else:
            inputs[name] = 1

    outputs = []
    for _ in range(max_x + 2):
        outputs.append(None)

    return inputs, outputs

def parse_gates(gate_lines):
    gates = {}
    for gate_line in gate_lines.strip().split("\n"):
        gate = make_gate(gate_line)
        gates[gate.out] = gate
    return gates

def make_gate(gate_line):
    rule, output = gate_line.split("->")
    left, op, right = rule.split()
    return Gate(left, right, op, output.strip(), None)

def do_gate(op, left, right):
    if op == "AND":
        return left & right
    if op == "OR":
        return left | right
    if op == "XOR":
        return left ^ right
    raise ValueError(f"Unknown op: {op}")

def swap_outputs(gate, other_gate):
    tmp_val = other_gate.value
    other_gate.value = gate.value
    gate.value = tmp_val

def find_swap_partner(gates, swaps, first_gate):
    index = swaps.index(first_gate.out)
    if index % 2 == 0:
        other = swaps[index + 1]
    else:
        other = swaps[index - 1]
    return gates[other]

def find_val(name, gates, inputs, swaps):
    if name in inputs:
        return inputs[name]

    return calc_output(gates[name], gates, inputs, swaps, True)

def calc_output(gate, gates, inputs, swaps, do_swap):
    if gate.value is None:
        val1 = find_val(gate.in1, gates, inputs, swaps)
        val2 = find_val(gate.in2, gates, inputs, swaps)
        gate.value = do_gate(gate.op, val1, val2)

        if do_swap and gate.out in swaps:
            other_gate = find_swap_partner(gates, swaps, gate)
            calc_output(other_gate, gates, inputs, swaps, False)
            swap_outputs(gate, other_gate)

    return gate.value

def propagate_signals(gates, inputs, outputs, swaps):
    for name, gate in gates.items():
        if name.startswith("z"):
            outputs[int(name[1:3])] = calc_output(gate, gates, inputs, swaps, True)

    return outputs

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    inputs, outputs = generate_inputs(input_lines)
    gates = parse_gates(gate_lines)

    counter = 0
    for swaps in combinations(gates.keys(), 8):
        outputs = propagate_signals(gates, inputs, outputs, swaps)

        counter += 1
        if counter % 10000 == 0:
            # trick courtesy ChatGPT
            print(int("".join(map(str, reversed(outputs))), 2))

        for gate in gates.values():
            gate.value = None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
