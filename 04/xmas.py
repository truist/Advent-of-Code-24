#!/usr/bin/env python3

"""
Advent of Code 2024-04
"""

import argparse

horizontals = {}
verticals = {}
diag1 = {}
diag2 = {}

def bundle_strings(group):
    """
    extract the strings from a group into a simple array
    """
    return [group[key] for key in sorted(group.keys())]

def register_char_in(char, cell_sum, group):
    """
    add a character to a single directional group
    """
    if cell_sum not in group:
        group[cell_sum] = ""
    group[cell_sum] += char

def register_char(char, row, col):
    """
    add a character to each of the four directional groups
    """
    register_char_in(char, row, horizontals)
    register_char_in(char, col, verticals)
    register_char_in(char, row + col, diag1)
    register_char_in(char, col - row, diag2)

def count_xmas(grid):
    """
    collect up lists of strings in all four directions (horizontal, vertical, both diagonals),
    then count 'XMAS' forward and reverse in each string
    """
    width = len(grid[0])
    height = len(grid)

    for row in range(height):
        for col in range(width):
            register_char(grid[row][col], row, col)

    strings = bundle_strings(horizontals) \
        + bundle_strings(verticals) \
        + bundle_strings(diag1) \
        + bundle_strings(diag2)

    match_count = 0
    for string in strings:
        match_count += string.count("XMAS")
        match_count += string.count("SAMX")

    return match_count


def main(inputfile):
    """
    Process the input data
    """
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    print(count_xmas(grid))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-04")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
