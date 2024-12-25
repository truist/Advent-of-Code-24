#!/usr/bin/env python3

"""
Advent of Code 2024-24
"""

import argparse
from dataclasses import dataclass
from itertools import combinations
from itertools import permutations
from collections import deque
from collections import defaultdict

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
    inputs: dict
    outputs: list

    def input_bit_indexes(self):
        yield from range(len(self.outputs) - 1)

    def bit_name(self, prefix, index):
        return f"{prefix}{index:02}"

    def reset_inputs(self):
        for i in self.input_bit_indexes():
            self.inputs[self.bit_name("x", i)] = 0
            self.inputs[self.bit_name("y", i)] = 0

    def reset_signals(self):
        for gate in self.gates.values():
            gate.value = None

    def z_gates(self):
        for index in range(len(self.outputs)): # pylint: disable=consider-using-enumerate
            yield index, self.gates[self.bit_name("z", index)]

    def find_val(self, name, swaps):
        if name in self.inputs:
            return self.inputs[name]

        return self.calc_output(self.gates[name], swaps, True)

    def find_swap_partner(self, first_gate, swaps):
        index = swaps.index(first_gate.out)
        if index % 2 == 0:
            other = swaps[index + 1]
        else:
            other = swaps[index - 1]
        return self.gates[other]

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

    def propagate_signals(self, swaps, output_bits):
        self.reset_signals()
        for index, gate in self.z_gates():
            if index in output_bits:
                self.outputs[index] = self.calc_output(gate, swaps, True)

    def test_bit(self, bit, swaps):
        # print(f"testing bit {bit}")
        self.reset_inputs()

        addr_tests = {
            (0, 0): (0, 0),
            (0, 1): (1, 0),
            (1, 0): (1, 0),
            (1, 1): (0, 1),
        }
        for case_input, case_output in addr_tests.items():
            self.inputs[self.bit_name("x", bit)] = case_input[0]
            self.inputs[self.bit_name("y", bit)] = case_input[1]

            self.propagate_signals(swaps, (bit, bit + 1))

            actual_output = (self.outputs[bit], self.outputs[bit + 1])
            if actual_output != case_output:
                # print(f"found error in bit {bit}: {actual_output} was not {case_output}")
                return False

        return True

    def streams(self, bit, up):
        found = set()
        queue = deque()

        starts = ("z") if up else ("x", "y")
        for prefix in starts:
            queue.append(self.bit_name(prefix, bit))

        while queue:
            name = queue.popleft()

            gates = []
            if up:
                if name in self.gates and name not in found:
                    found.add(name)
                    gates.append(self.gates[name])
            else:
                for gate in self.gates.values():
                    if name in (gate.in1, gate.in2) and gate.out not in found:
                        found.add(gate.out)
                        gates.append(gate)

            for gate in gates:
                queue.append(gate.in1)
                queue.append(gate.in2)

        # print(f"found these {up}-streams: {found}")
        # duplicates = list({item.out for item in found if found.count(item) > 1})
        # if len(duplicates) > 0:
        #     print(f"found duplicate {up}-streams: {duplicates}")
        return found


def generate_inputs(input_lines):
    inputs = {}
    max_x = 0
    for input_line in input_lines.split("\n"):
        name, _ = input_line.split(":")
        name = name.strip()
        inputs[name] = 0
        max_x = max(max_x, int(name[1:3]))

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

def make_circuit(input_lines, gate_lines):
    inputs, outputs = generate_inputs(input_lines)
    gates = parse_gates(gate_lines)
    return Circuit(gates, inputs, outputs)

# def bits_to_decimal(bits):
#     return int("".join(map(str, bits)), 2)

# def propagate_to_zero(circuits, swaps):
#     min_zero = len(circuits[0].outputs) + 1
#     for circuit in circuits:
#         min_zero = min(min_zero, circuit.propagate_to_zero(swaps))
#     return min_zero

# def find_swaps(index, circuits, swaps):
#     print(f"looking for swap to fix bit {index}")
#     print(f"known swaps: {swaps}")
#     for new_swaps in combinations(circuits[0].gates.keys(), 2):
#         if new_swaps[0] in swaps or new_swaps[1] in swaps:
#             continue

#         combined_swaps = list(new_swaps) + swaps
#         next_zero = propagate_to_zero(circuits, combined_swaps)
#         if next_zero > index:
#             # print(f"found swap! {new_swaps}")
#             # print("circuit 1 outputs:", circuit1.outputs, bits_to_decimal(circuit1.outputs))
#             # print("circuit 2 outputs:", circuit2.outputs, bits_to_decimal(circuit2.outputs))

#             downstream_swaps = handle_zeros(next_zero, circuits, combined_swaps)
#             if downstream_swaps is not None:
#                 print("success at the end!")
#                 return downstream_swaps

#     print(f"can't find suitable swaps for {index}")
#     return None

# def handle_zeros(next_zero, circuits, swaps):
#     if next_zero == len(circuits[0].outputs - 1):
#         print("no more zeros!")
#         return swaps

#     if len(swaps) == 8:
#         # print("hit swap limit")
#         return None

#     downstream_swaps = find_swaps(next_zero, circuits, swaps)
#     if downstream_swaps is not None:
#         print("success at the end!")
#         return downstream_swaps

#     print(f"couldn't handle the zero at {next_zero}")
#     return None

def find_problem_gate_candidates(circuit):
    input_downstreams = set()
    output_upstreams = set()
    for bit in circuit.input_bit_indexes():
        if not circuit.test_bit(bit, []):
            print(f"found bad bit: {bit}")
            input_downstreams |= circuit.streams(bit, False)
            output_upstreams |= circuit.streams(bit, True)
            output_upstreams |= circuit.streams(bit + 1, True)

    # print(sorted(input_downstreams))
    # print(sorted(output_upstreams))
    candidates = sorted(list(input_downstreams | output_upstreams)) # XXX FIXME should be &
    print(candidates)
    return candidates

def find_first_bad_bit(circuit, known_swaps):
    for bit in circuit.input_bit_indexes():
        if not circuit.test_bit(bit, known_swaps):
            return bit
    return -1

def try_swap(test_swap, circuit, candidates, known_swaps, first_bad_bit):
    candidates = [candidate for candidate in candidates if candidate not in test_swap]
    known_swaps = list(known_swaps) + list(test_swap)
    # print(f"test known_swaps at {first_bad_bit}: {known_swaps}")
    return find_swaps(circuit, candidates, known_swaps, first_bad_bit)

def find_swaps(circuit, candidates, known_swaps, min_bad_bit):
    # print(f"testing swaps at {min_bad_bit} with {len(candidates)} candidates and {len(known_swaps)} known swaps")
    if len(known_swaps) > 8:
        # print(f"too many swaps: {len(known_swaps)}")
        return None

    first_bad_bit = find_first_bad_bit(circuit, known_swaps)

    if first_bad_bit < 0:
        print(f"no bad bits! {known_swaps}")
        return known_swaps

    if first_bad_bit <= min_bad_bit:
        # print(f"found early-bad bit at {bit}")
        return None

    print(f"got a new bad bit: {first_bad_bit} with {len(known_swaps)} known swaps and {len(candidates)} candidates")
    for test_swap in combinations(candidates, 2):
        found_swaps = try_swap(test_swap, circuit, candidates, known_swaps, first_bad_bit)
        if found_swaps is not None:
            print(f"found swaps! {found_swaps}, {known_swaps}")
            return found_swaps

    print(f"no test swaps worked at {first_bad_bit}")
    return None

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    circuit = make_circuit(input_lines, gate_lines)
    candidates = find_problem_gate_candidates(circuit)

    print(find_swaps(circuit, candidates, [], -1))


    return
    for swaps in permutations(candidates, 8):
        # print(f"trying swaps {swaps}")
        found_it = True
        for bit in circuit.input_bit_indexes():
            if not circuit.test_bit(bit, swaps):
                found_it = False
                break

        if found_it:
            print("found it! {swaps}")
            break



    # print_gates(circuits[0])

    return
    swaps = []
    next_zero = propagate_to_zero(circuits, swaps)
    for circuit in circuits:
        print(circuit.outputs)

    swaps = handle_zeros(next_zero, circuits, swaps)
    for circuit in circuits:
        print(circuit.outputs)
    print(swaps)


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
