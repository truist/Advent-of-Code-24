#!/usr/bin/env python3

"""
Advent of Code 2024-19
"""

import argparse

def can_make(pattern, towels):
    if len(pattern) == 0:
        return True
    for towel in towels:
        if pattern.startswith(towel):
            new_start = len(towel)
            if can_make(pattern[new_start:], towels):
                return True

    return False

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        towels, patterns = file.read().split("\n\n")
        towels = [towel.strip() for towel in towels.split(",")]
        patterns = patterns.strip().split("\n")
    # print(towels)
    # print(patterns)

    can_do = 0
    for pattern in patterns:
        # print(f"testing {pattern}")
        if can_make(pattern, towels):
            can_do += 1

    print(can_do)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-19")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
