#!/usr/bin/env python3

"""
Advent of Code 2024-04
"""

import argparse

def test_diag(grid, row, col, x_offset, y_offset):
    """
    test a given spot for MAS in both diagonal directions
    """
    first = grid[row - y_offset][col - x_offset]
    second = grid[row + y_offset][col + x_offset]
    return (first == "M" and second == "S") or (first == "S" and second == "M")

def count_xmas(grid):
    """
    count the number of times MAS appears in both diagnal directions
    """
    width = len(grid[0])
    height = len(grid)

    match_count = 0
    for row in range(1, height - 1):
        for col in range(1, width - 1):
            if grid[row][col] == "A":
                if test_diag(grid, row, col, 1, 1) and test_diag(grid, row, col, -1, 1):
                    match_count += 1

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
