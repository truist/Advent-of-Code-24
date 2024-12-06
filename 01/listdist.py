#!/usr/bin/env python3

"""
a module docstring
"""

import argparse


def main(inputfile):
    """
    a function docstring
    """

    left = []
    right = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            (l, r) = line.split()
            left.append(int(l))
            right.append(int(r))

    left.sort()
    right.sort()

    distance = 0
    for l, r in zip(left, right):
        distance += abs(r - l)

    print(f"Total distance: {distance}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-01")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
