#!/usr/bin/env python3

"""
Advent of Code 2024-NEWDAY
"""

import argparse


def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    print(grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-NEWDAY")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
