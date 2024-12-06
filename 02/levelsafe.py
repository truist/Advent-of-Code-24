#!/usr/bin/env python3

"""
Advent of Code 2024-02
"""

import argparse

def safe(report):
    """
    Calculate whether a report is safe
    """
    if len(report) < 2:
        # only 1 report; let's assume that counts as safe
        return 1

    increasing = report[1] > report[0]
    last_level = report[0]

    for level in report[1:]:
        if (level > last_level) != increasing:
            return 0

        diff = abs(level - last_level)
        if diff < 1 or diff > 3:
            return 0

        last_level = level

    return 1


def main(inputfile):
    """
    Process the input data
    """

    reports = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            reports.append([int(strint) for strint in line.split()])

    totalsafe = 0
    for r in reports:
        totalsafe += safe(r)

    print(f"Total safe: {totalsafe}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-02")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
