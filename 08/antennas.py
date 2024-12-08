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

def find_antinodes_in_direction(direction, cur_row, row_offset, max_rows, cur_col, col_offset, max_cols):
    in_bounds = []
    while True:
        cur_row = cur_row + row_offset * direction
        cur_col = cur_col + col_offset * direction

        if 0 <= cur_row < max_rows and 0 <= cur_col < max_cols:
            in_bounds += [(cur_row, cur_col)]
        else:
            break

    return in_bounds

def find_antinodes_for_pair(left, right, max_rows, max_cols):
    row_offset = right[0] - left[0]
    col_offset = right[1] - left[1]

    in_bounds = [left, right]
    in_bounds += find_antinodes_in_direction(1, left[0], row_offset, max_rows, left[1], col_offset, max_cols)
    in_bounds += find_antinodes_in_direction(-1, left[0], row_offset, max_rows, left[1], col_offset, max_cols)

    # print(f"{left}, {right} gave {in_bounds}")

    return in_bounds

def find_all_antinodes(all_antennas, max_rows, max_cols):
    antinodes = []
    for antennas in all_antennas.values():
        for l, left in enumerate(antennas[0:-1]):
            for right in antennas[l+1:]:
                antinodes += find_antinodes_for_pair(left, right, max_rows, max_cols)

    return antinodes


def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    antennas = find_antennas(grid)
    antinodes = find_all_antinodes(antennas, len(grid), len(grid[0]))
    # print(antinodes)

    print(len(set(antinodes)))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-08")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
