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

# basically just a holder for globals
@dataclass
class Circuit:
    gates: list
    inputs: list
    outputs: list

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

def make_gate(gate_line):
    rule, output = gate_line.split("->")
    left, op, right = rule.split()
    return Gate(left, right, op, output.strip(), None)

def parse_gates(gate_lines):
    gates = {}
    for gate_line in gate_lines.strip().split("\n"):
        gate = make_gate(gate_line)
        gates[gate.out] = gate
    return gates

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

def find_val(name, circuit, swaps):
    if name in circuit.inputs:
        return circuit.inputs[name]

    return calc_output(circuit.gates[name], circuit, swaps, True)

def calc_output(gate, circuit, swaps, do_swap):
    if gate.value is None:
        val1 = find_val(gate.in1, circuit, swaps)
        val2 = find_val(gate.in2, circuit, swaps)
        gate.value = do_gate(gate.op, val1, val2)

        if do_swap and gate.out in swaps:
            other_gate = find_swap_partner(circuit.gates, swaps, gate)
            calc_output(other_gate, circuit, swaps, False)
            swap_outputs(gate, other_gate)

    return gate.value

def propagate_signals(circuit, swaps):
    reset_signals(circuit.gates)
    for name, gate in circuit.gates.items():
        if name.startswith("z"):
            circuit.outputs[int(name[1:3])] = calc_output(gate, circuit, swaps, True)

def reset_signals(gates):
    for gate in gates.values():
        gate.value = None

def find_upstreams(name, gates):
    if name not in gates:
        return []
    gate = gates[name]
    return [name] + find_upstreams(gate.in1, gates) + find_upstreams(gate.in2, gates)

def bits_to_decimal(bits):
    return int("".join(map(str, bits)), 2)

def find_swaps(index, circuit, swaps):
    print(f"looking for swap to fix bit {index}")
    # print(f"known swaps: {swaps}")
    for new_swaps in combinations(circuit.gates.keys(), 2):
        if new_swaps[0] in swaps or new_swaps[1] in swaps:
            continue
        all_swaps = list(new_swaps) + swaps
        propagate_signals(circuit, all_swaps)
        # print(bits_to_decimal(outputs))
        if 0 not in circuit.outputs[0:index + 1]:
            # print(f"found swap! {new_swaps}")
            # print(f"fixed bit {index}: {outputs}")
            try:
                next_zero = circuit.outputs.index(0, index + 1)
            except ValueError:
                print("no more zeros!")
                return all_swaps

            downstream_swaps = find_swaps(next_zero, circuit, all_swaps)
            if downstream_swaps is not None:
                print("success at the end!")
                return downstream_swaps

    print("reached the end and couldn't find a swap")
    return None

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    inputs, outputs = generate_inputs(input_lines)
    gates = parse_gates(gate_lines)
    circuit = Circuit(gates, inputs, outputs)

    swaps = []
    propagate_signals(circuit, swaps)
    print(circuit.outputs)

    swaps = find_swaps(circuit.outputs.index(0), circuit, swaps)
    print(circuit.outputs)

    print(swaps)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
