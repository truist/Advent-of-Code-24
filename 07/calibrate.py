#!/usr/bin/env python3

"""
Advent of Code 2024-07
"""

import argparse

def check_operations(desired, values):
    # print(f"testing {desired} = {values}")
    if desired % 1 != 0 or desired < 0:
        return False
    desired = int(desired)

    if len(values) == 1:
        return desired == values[0]

    if check_operations(desired - values[-1], values[0:-1]):
        # print(f"True: add: {desired} = {values}")
        return True

    if check_operations(desired / values[-1], values[0:-1]):
        # print(f"True: multiply: {desired} = {values}")
        return True

    right = str(values[-1])
    if str(desired).endswith(right):
        left = str(desired)[:-len(right)]
        if check_operations(int(left), values[0:-1]):
            # print(f"True: concatenated: {desired} = {values}")
            return True

    return False

def main(inputfile):
    total = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            (desired, values) = line.split(":")
            desired = int(desired)
            values = [int(s) for s in values.split()]
            if check_operations(desired, values):
                # print(f"got {desired} = {values}")
                total += desired

    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-07")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
