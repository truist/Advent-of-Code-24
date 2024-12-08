#!/usr/bin/env python3

"""
Advent of Code 2024-06
"""

import argparse

def find_start(grid, start_char):
    width = len(grid[0])
    height = len(grid)

    for row in range(height):
        for col in range(width):
            if grid[row][col] == start_char:
                return (row, col)

    raise KeyError("No matching start_char")

def stepping_off_edge(grid, row, col, direction):
    if direction == "N" and row == 0:
        return True
    if direction == "E" and col == len(grid[0]):
        return True
    if direction == "S" and row == len(grid) - 1:
        return True
    if direction == "W" and col == 0:
        return True
    return False

def turn_if_blocked(grid, row, col, direction):
    if direction == "N" and grid[row - 1][col] == "#":
        return "E"
    if direction == "E" and grid[row][col + 1] == "#":
        return "S"
    if direction == "S" and grid[row + 1][col] == "#":
        return "W"
    if direction == "W" and grid[row][col - 1] == "#":
        return "N"
    return direction

def take_step(row, col, direction):
    if direction == "N":
        return (row - 1, col)
    if direction == "E":
        return (row, col + 1)
    if direction == "S":
        return (row + 1, col)
    if direction == "W":
        return (row, col - 1)
    raise ValueError(f"No such direction {direction}")

def find_path_length(grid, row, col, direction):
    length = 1
    while True:
        grid[row][col] = "X"

        if stepping_off_edge(grid, row, col, direction):
            break

        direction = turn_if_blocked(grid, row, col, direction)
        (row, col) = take_step(row, col, direction)

        if grid[row][col] != "X":
            length += 1

    return length

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    (row, col) = find_start(grid, "^")
    print(find_path_length(grid, row, col, "N"))
    # print(grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-06")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
