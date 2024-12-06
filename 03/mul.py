#!/usr/bin/env python3

"""
Advent of Code 2024-03
"""

import argparse
import re

def main(inputfile):
    """
    Process the input data
    """
    with open(inputfile, 'r', encoding='utf-8') as file:
        content = file.read()

    total = 0
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    for match in re.finditer(pattern, content):
        total += int(match.group(1)) * int(match.group(2))

    print(f"total: {total}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-03")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
