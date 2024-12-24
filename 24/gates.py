#!/usr/bin/env python3

"""
Advent of Code 2024-24
"""

import argparse
from dataclasses import dataclass

@dataclass
class Gate:
    in1: str
    in2: str
    op: str
    out: str
    value: int

def parse_inputs(input_lines):
    inputs = {}
    for input_line in input_lines.split("\n"):
        name, value = input_line.split(":")
        inputs[name.strip()] = int(value.strip())
    return inputs

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

def find_val(name, gates, inputs):
    if name in inputs:
        return inputs[name]

    return calc_output(gates[name], gates, inputs)

def calc_output(gate, gates, inputs):
    if gate.value is None:
        val1 = find_val(gate.in1, gates, inputs)
        val2 = find_val(gate.in2, gates, inputs)
        gate.value = do_gate(gate.op, val1, val2)

    return gate.value

def propagate_signals(gates, inputs):
    z_names = []
    for name, gate in gates.items():
        if name.startswith("z"):
            z_names.append(name)
            calc_output(gate, gates, inputs)

    bits = []
    for name in reversed(sorted(z_names)):
        bits.append(gates[name].value)
    return bits


def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    inputs = parse_inputs(input_lines)
    gates = parse_gates(gate_lines)

    bits = propagate_signals(gates, inputs)

    # trick courtesy ChatGPT
    print(int("".join(map(str, bits)), 2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
