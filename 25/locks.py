#!/usr/bin/env python3

"""
Advent of Code 2024-25
"""

import argparse

def parse_lock(grid):
    heights = []
    for c in range(len(grid[0])):
        for r in range(len(grid)): # pylint: disable=consider-using-enumerate
            if grid[r][c] != "#":
                heights.append(r - 1)
                break
    return heights

def parse_key(grid):
    grid.reverse()
    return parse_lock(grid)

def is_compatible(lock, key):
    for c, height in enumerate(lock):
        if key[c] + height > 5:
            return False
    return True

def count_compatible(locks, keys):
    compatible = 0
    for lock in locks:
        for key in keys:
            if is_compatible(lock, key):
                compatible += 1
    return compatible

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        blobs = file.read().split("\n\n")

    locks = []
    keys = []
    for blob in blobs:
        grid = [list(line.strip()) for line in blob.strip().split("\n")]
        if "." in grid[0]:
            keys.append(parse_key(grid))
        else:
            locks.append(parse_lock(grid))

    print(count_compatible(locks, keys))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-25")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
