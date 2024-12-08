#!/usr/bin/env python3

"""
Advent of Code 2024-08
"""

import argparse

def add_antenna(antennas, value, row, col):
    if value not in antennas:
        antennas[value] = []

    antennas[value] += [(row, col)]

def find_antennas(grid):
    antennas = {}
    for row, row_data in enumerate(grid):
        for col, value in enumerate(row_data):
            if value != ".":
                add_antenna(antennas, value, row, col)

    return antennas

def find_antinodes(left, right, max_rows, max_cols):
    # (1,8) (2,5)
    row_offset = right[0] - left[0] # 1
    col_offset = right[1] - left[1] # -3

    one = (left[0] - row_offset, left[1] - col_offset) # (0, 11)
    two = (right[0] + row_offset, right[1] + col_offset) # (3, 2)

    in_bounds = []
    if 0 <= one[0] < max_rows and 0 <= one[1] < max_cols:
        in_bounds += [one]
    if 0 <= two[0] < max_rows and 0 <= two[1] < max_cols:
        in_bounds += [two]

    # print(f"{left}, {right} gave {in_bounds}")

    return in_bounds

def find_all_antinodes(all_antennas, max_rows, max_cols):
    antinodes = []
    for antennas in all_antennas.values():
        for l, left in enumerate(antennas[0:-1]):
            for right in antennas[l+1:]:
                antinodes += find_antinodes(left, right, max_rows, max_cols)

    return antinodes


def main(inputfile):
    total = 0
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    antennas = find_antennas(grid)
    # print(antennas)
    antinodes = find_all_antinodes(antennas, len(grid), len(grid[0]))
    # print(antinodes)

    print(len(set(antinodes)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-08")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
