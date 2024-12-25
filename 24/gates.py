#!/usr/bin/env python3

"""
Advent of Code 2024-24
"""

import argparse
from dataclasses import dataclass
from itertools import combinations
from collections import deque

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

    def set_inputs(self, x_vals, y_vals):
        for i in self.input_bit_indexes():
            self.inputs[self.bit_name("x", i)] = x_vals[i] if i < len(x_vals) else 0
            self.inputs[self.bit_name("y", i)] = y_vals[i] if i < len(y_vals) else 0

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

            if up:
                if name in self.gates and name not in found:
                    found.add(name)
                    gate = self.gates[name]
                    queue.append(gate.in1)
                    queue.append(gate.in2)
            else:
                for gate in self.gates.values():
                    if name in (gate.in1, gate.in2) and gate.out not in found:
                        found.add(gate.out)
                        queue.append(gate.out)

        # print(f"found these {up}-streams: {found}")
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

def find_problem_gate_candidates(circuit):
    candidates = set()
    for bit in circuit.input_bit_indexes():
        if not circuit.test_bit(bit, []):
            # print(f"found bad bit: {bit}")
            input_downstreams = circuit.streams(bit, False)
            output_upstreams = circuit.streams(bit, True)
            output_upstreams |= circuit.streams(bit + 1, True)
            # print(sorted(input_downstreams))
            # print(sorted(output_upstreams))
            candidates |= (input_downstreams & output_upstreams)

    # print(sorted(input_downstreams))
    # print(sorted(output_upstreams))
    # candidates = list(input_downstreams & output_upstreams)
    candidates = sorted(candidates)
    # print(f"candidates: {candidates}")
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
        # print(f"no bad bits! {known_swaps}")
        if verify_result(circuit, known_swaps):
            # print("verified result!")
            # print(",".join(sorted(known_swaps)))
            return known_swaps
        return None

    if first_bad_bit <= min_bad_bit:
        # print(f"found early-bad bit at {bit}")
        return None

    # print(f"got a new bad bit: {first_bad_bit} with {len(known_swaps)} known swaps and {len(candidates)} candidates")
    successful_swaps = None
    for test_swap in combinations(candidates, 2):
        found_swaps = try_swap(test_swap, circuit, candidates, known_swaps, first_bad_bit)
        if found_swaps is not None:
            # print(f"found swaps for {first_bad_bit}! {found_swaps}, {known_swaps}")
            return found_swaps
            # if successful_swaps is not None:
            #     print(f"found a second successful swap for {first_bad_bit}! {successful_swaps}; {found_swaps}")
            # successful_swaps = found_swaps
    return successful_swaps

    # print(f"no test swaps worked at {first_bad_bit}")
    # return None

def to_decimal(binary):
    return int("".join([str(val) for val in reversed(binary)]), 2)

def str_to_int_array(string):
    return [int(val) for val in string]

def verify_result(circuit, swaps):
    input_len = len(circuit.outputs) - 1
    zeroes = str_to_int_array("0" * input_len)
    ones = str_to_int_array("1" * input_len)
    evens = str_to_int_array("10" * (input_len // 2))
    odds = str_to_int_array("01" * (input_len // 2))

    test_cases = [
        (zeroes, zeroes),
        (zeroes, ones),
        (ones, zeroes),
        (ones, ones),
        (evens, evens),
        (odds, odds),
        (evens, odds),
        (odds, evens),
        (ones, evens),
        (ones, odds),
        (odds, ones),
        (evens, ones),
    ]
    for val1, val2 in test_cases:
        circuit.set_inputs(val1, val2)
        circuit.propagate_signals(swaps, list(range(input_len + 1)))

        dval1 = to_decimal(val1)
        dval2 = to_decimal(val2)
        doutput = to_decimal(circuit.outputs)
        dexpected = dval1 + dval2
        if dval1 + dval2 != doutput:
            # print(f"{dval1} + {dval2} gave {doutput} but should have been {dexpected}")
            # print(val1)
            # print(val2)
            # print(circuit.outputs)
            # print(list(reversed([int(val) for val in bin(dexpected)[2:]])))
            return False
    return True

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        input_lines, gate_lines = file.read().split("\n\n")

    circuit = make_circuit(input_lines, gate_lines)
    candidates = find_problem_gate_candidates(circuit)

    swaps = find_swaps(circuit, candidates, [], -1)
    print(",".join(sorted(swaps)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-24")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
