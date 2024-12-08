#!/usr/bin/env python3

"""
Advent of Code 2024-06
"""

import argparse

def find_start(grid, start_char):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == start_char:
                return (row, col)

    raise KeyError("No matching start_char")

def stepping_off_edge(grid, row, col, direction):
    if direction == "N" and row == 0:
        return True
    if direction == "E" and col == len(grid[0]) - 1:
        return True
    if direction == "S" and row == len(grid) - 1:
        return True
    if direction == "W" and col == 0:
        return True
    return False

def turn_if_blocked(grid, row, col, direction):
    if direction == "N" and grid[row - 1][col] == "#":
        return turn_if_blocked(grid, row, col, "E")
    if direction == "E" and grid[row][col + 1] == "#":
        return turn_if_blocked(grid, row, col, "S")
    if direction == "S" and grid[row + 1][col] == "#":
        return turn_if_blocked(grid, row, col, "W")
    if direction == "W" and grid[row][col - 1] == "#":
        return turn_if_blocked(grid, row, col, "N")
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
    repeated_steps = 0
    repeated_step_max = 10000  # HACK
    while repeated_steps < repeated_step_max:
        grid[row][col] = "X"

        if stepping_off_edge(grid, row, col, direction):
            break

        direction = turn_if_blocked(grid, row, col, direction)
        (row, col) = take_step(row, col, direction)

        if grid[row][col] != "X":
            length += 1
        else:
            repeated_steps += 1

    if repeated_steps >= repeated_step_max:
        return -1
    return length

def find_obstacle_locations(grid, start_row, start_col, direction):
    obstacle_count = 0
    grid_copy = [row[:] for row in grid]
    for row, whole_row in enumerate(grid):
        for col, value in enumerate(whole_row):
            if row == start_row and col == start_col:
                continue
            if value == "X":
                if evaluate_obsctacle(grid_copy, row, col, start_row, start_col, direction):
                    obstacle_count += 1

    return obstacle_count

def evaluate_obsctacle(grid, row, col, start_row, start_col, direction):
    grid[row][col] = "#"
    obstacle_length = find_path_length(grid, start_row, start_col, direction)
    grid[row][col] = "X"

    return obstacle_length < 0

def print_grid(grid):
    for row in grid:
        print("".join(row))
    print("")

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    (start_row, start_col) = find_start(grid, "^")
    print(find_path_length(grid, start_row, start_col, "N"))
    # print_grid(grid)

    print(find_obstacle_locations(grid, start_row, start_col, "N"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-06")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
