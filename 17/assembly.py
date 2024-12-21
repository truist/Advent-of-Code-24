#!/usr/bin/env python3

"""
Advent of Code 2024-17
"""

import argparse
from dataclasses import dataclass

@dataclass
class Machine:
    a: int
    b: int
    c: int
    tape: list
    ip: int
    output: list

    def combo(self, operand):
        if operand < 4:
            return operand

        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c

        raise ValueError(f"Unrecognized combo operand: {operand}")

    def adv(self, operand): # 0
        self.a = self.a // pow(2, self.combo(operand))

    def bxl(self, operand): # 1
        self.b = self.b ^ operand

    def bst(self, operand): # 2
        self.b = self.combo(operand) % 8

    def jnz(self, operand): # 3
        if self.a == 0:
            self.ip += 2
            return
        self.ip = operand

    def bxc(self, operand): # 4  # pylint: disable=unused-argument
        self.b = self.b ^ self.c

    def out(self, operand): # 5
        self.output.append(self.combo(operand) % 8)

    def cdv(self, operand): # 7
        self.c = self.a // pow(2, self.combo(operand))

    def instruction(self):
        instr = self.tape[self.ip]
        operand = self.tape[self.ip + 1]
        if instr == 3:
            self.jnz(operand)
        else:
            if instr == 0:
                self.adv(operand)
            elif instr == 1:
                self.bxl(operand)
            elif instr == 2:
                self.bst(operand)
            elif instr == 4:
                self.bxc(operand)
            elif instr == 5:
                self.out(operand)
            elif instr == 6:
                raise ValueError(f"Unimplemented instruction: {instr}")
            elif instr == 7:
                self.cdv(operand)
            else:
                raise ValueError(f"Unrecognized instruction: {instr}")

            self.ip += 2

    def execute(self):
        while self.ip < len(self.tape) - 1:
            # print(self)
            self.instruction()

    def execute_until_first_output(self):
        while self.ip < len(self.tape) - 1:
            self.instruction()
            if len(self.output) > 0:
                return self.output[0]
        raise ValueError("Program terminated before generating output!")

def extract_register_value(line):
    _, right = line.split(":")
    return int(right.strip())

def test_input(template_machine, test_value):
    machine = Machine(
        test_value,
        template_machine.b,
        template_machine.c,
        template_machine.tape,
        0,
        []
    )
    return machine.execute_until_first_output()

def find_magic_value(template_machine, start, goals):
    for offset in range(8):
        test_value = start + offset
        if test_input(template_machine, test_value) == goals[0]:
            if len(goals) == 1:
                return test_value
            result = find_magic_value(template_machine, test_value * 8, goals[1:])
            if result is not None:
                return result

    return None

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        registers, program = file.read().split("\n\n")

        a, b, c = registers.split("\n")
        a = extract_register_value(a)
        b = extract_register_value(b)
        c = extract_register_value(c)

        _, right = program.split(":")
        tape = [int(val) for val in right.strip().split(",")]

        # machine = Machine(a, b, c, tape, 0, [])

    template_machine = Machine(a, b, c, tape, 0, [])
    goals = list(reversed(tape))
    found_value = find_magic_value(template_machine, 1, goals)

    print(f"found value {found_value}, trying it...")
    machine = Machine(found_value, b, c, tape, 0, [])
    machine.execute()
    print(tape)
    print(machine.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-17")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)


"""
Program: 2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0

B = A % 8
B = B ^ 3
C = A // 2^B
B = B ^ C
B = B ^ 3
A = A // 8
output B % 8
if A > 0 goto beginning

while A = A // 8 > 0:
    output = ((((A % 8) ^ 3) ^ (A // (2 ** ((A % 8) ^ 3)))) ^ 3) % 8
"""


