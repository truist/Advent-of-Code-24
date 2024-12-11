#!/usr/bin/env python3

"""
Advent of Code 2024-10
"""

import argparse

def try_step(grid, r, c, new_r, new_c):
    if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
        if grid[new_r][new_c] == grid[r][c] + 1:
            if grid[new_r][new_c] == 9:
                return [(new_r, new_c)]
            return find_reachable_nines(grid, new_r, new_c)

    return []

def find_reachable_nines(grid, r, c):
    reachable = []
    reachable += try_step(grid, r, c, r - 1, c)
    reachable += try_step(grid, r, c, r + 1, c)
    reachable += try_step(grid, r, c, r, c - 1)
    reachable += try_step(grid, r, c, r, c + 1)

    return reachable


def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [[int(val) for val in line.strip()] for line in file]

    score = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == 0:
                score += len(set(find_reachable_nines(grid, r, c)))

    print(score)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-10")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
