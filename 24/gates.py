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

    def calculate(self, left, right):
        if self.op == "AND":
            return left & right
        if self.op == "OR":
            return left | right
        if self.op == "XOR":
            return left ^ right
        raise ValueError(f"Unknown op: {self.op}")

    def swap_outputs(self, other_gate):
        tmp_val = other_gate.value
        other_gate.value = self.value
        self.value = tmp_val


# basically just a holder for globals
@dataclass
class Circuit:
    gates: dict
    inputs: list
    outputs: list

    def reset_signals(self):
        for gate in self.gates.values():
            gate.value = None

    def find_swap_partner(self, first_gate, swaps):
        index = swaps.index(first_gate.out)
        if index % 2 == 0:
            other = swaps[index + 1]
        else:
            other = swaps[index - 1]
        return self.gates[other]

    def find_val(self, name, swaps):
        if name in self.inputs:
            return self.inputs[name]

        return self.calc_output(self.gates[name], swaps, True)

    def calc_output(self, gate, swaps, do_swap):
        if gate.value is None:
            val1 = self.find_val(gate.in1, swaps)
            val2 = self.find_val(gate.in2, swaps)
            gate.value = gate.calculate(val1, val2)

            if do_swap and gate.out in swaps:
                other_gate = self.find_swap_partner(gate, swaps)
                self.calc_output(other_gate, swaps, False)
                gate.swap_outputs(other_gate)

        return gate.value

    def z_gates(self):
        for index in range(len(self.outputs)): # pylint: disable=consider-using-enumerate
            yield index, self.gates[f"z{index:02}"]

    def propagate_to_zero(self, swaps):
        self.reset_signals()
        for index, gate in self.z_gates():
            result = self.calc_output(gate, swaps, True)
            self.outputs[index] = result
            if result == 0:
                return index
        return len(self.outputs) + 1

def generate_inputs(input_lines, even_x, odd_x, even_y, odd_y):
    inputs = {}
    max_x = 0
    index = 0
    for input_line in input_lines.split("\n"):
        name, _ = input_line.split(":")
        name = name.strip()
        if name.startswith("x"):
            inputs[name] = even_x if index % 2 == 0 else odd_x
            max_x = max(max_x, int(name[1:3]))
        else:
            inputs[name] = even_y if index % 2 == 0 else odd_y

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

def make_circuit(input_lines, gate_lines, even_x, odd_x, even_y, odd_y):
    inputs, outputs = generate_inputs(input_lines, even_x, odd_x, even_y, odd_y)
    gates = parse_gates(gate_lines)
    return Circuit(gates, inputs, outputs)

def bits_to_decimal(bits):
    return int("".join(map(str, bits)), 2)

def propagate_to_zero(circuits, swaps):
    min_zero = len(circuits[0].outputs) + 1
    for circuit in circuits:
        min_zero = min(min_zero, circuit.propagate_to_zero(swaps))
    return min_zero

def find_swaps(index, circuits, swaps):
    print(f"looking for swap to fix bit {index}")
    print(f"known swaps: {swaps}")
    for new_swaps in combinations(circuits[0].gates.keys(), 2):
        if new_swaps[0] in swaps or new_swaps[1] in swaps:
            continue

        combined_swaps = list(new_swaps) + swaps
        next_zero = propagate_to_zero(circuits, combined_swaps)
        if next_zero > index:
            # print(f"found swap! {new_swaps}")
            # print("circuit 1 outputs:", circuit1.outputs, bits_to_decimal(circuit1.outputs))
            # print("circuit 2 outputs:", circuit2.outputs, bits_to_decimal(circuit2.outputs))

            downstream_swaps = handle_zeros(next_zero, circuits, combined_swaps)
            if downstream_swaps is not None:
                print("success at the end!")
                return downstream_swaps

    print(f"can't find suitable swaps for {index}")
    return None

def handle_zeros(next_zero, circuits, swaps):
    if next_zero == len(circuits[0].outputs - 1):
        print("no more zeros!")
        return swaps

    if len(swaps) == 8:
        # print("hit swap limit")
        return None

    downstream_swaps = find_swaps(next_zero, circuits, swaps)
    if downstream_swaps is not None:
        print("success at the end!")
        return downstream_swaps

    print(f"couldn't handle the zero at {next_zero}")
    return None

def print_upstream(maybe_gate, gates, offset, increment):
    if maybe_gate in gates:
        return print_gate(gates[maybe_gate], gates, offset, increment)
    offset = " " * offset
    return f"{offset}{maybe_gate}"

def print_gate(gate, gates, offset, increment):
    up1 = print_upstream(gate.in1, gates, offset + increment, increment)
    up2 = print_upstream(gate.in2, gates, offset + increment, increment)

    if gate.in1 < gate.in2:
        return f"({up1} {gate.op} {up2})"
    return f"({up2} {gate.op} {up1})"
    # offset = " " * offset
    # return f"{offset}{gate.op}\n{up1}\n{up2}"

def print_gates(circuit):
    last_line = ""
    for index, gate in circuit.z_gates():
        line = print_gate(gate, circuit.gates, 0, 0)
        # print(f"{index}: {len(line)}")
        print(f"{index}: {len(line) - len(last_line)}")
        # print(f"{index}:", line)
        print(line)
        last_line = line

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    circuits = []
    circuits.append(make_circuit(input_lines, gate_lines, 1, 1, 0, 0))
    circuits.append(make_circuit(input_lines, gate_lines, 0, 0, 1, 1))
    circuits.append(make_circuit(input_lines, gate_lines, 1, 0, 0, 1))
    circuits.append(make_circuit(input_lines, gate_lines, 0, 1, 1, 0))

    # print_gates(circuits[0])

    swaps = []
    next_zero = propagate_to_zero(circuits, swaps)
    for circuit in circuits:
        print(circuit.outputs)

    swaps = handle_zeros(next_zero, circuits, swaps)
    for circuit in circuits:
        print(circuit.outputs)
    print(swaps)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
