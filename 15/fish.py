#!/usr/bin/env python3

"""
Advent of Code 2024-15
"""

import argparse

ROBOT = "@"
BOX = "O"
WALL = "#"
EMPTY = "."
N = "^"
E = ">"
S = "v"
W = "<"

def find_robot(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == ROBOT:
                return r, c

    raise ValueError("Robot not found!")

def get_step_for_direction(direction):
    if direction == N:
        return -1, 0
    if direction == E:
        return 0, 1
    if direction == S:
        return 1, 0
    if direction == W:
        return 0, -1
    raise ValueError(f"Illegal direction: {direction}")

def gather_line_ahead(grid, r, c, direction):
    rx, cx = get_step_for_direction(direction)
    r += rx
    c += cx

    cells = []
    while 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        cells += grid[r][c]
        r += rx
        c += cx

    return cells

def can_move(cells_ahead):
    for cell in cells_ahead:
        if cell == WALL:
            return False
        if cell != BOX:
            return True
    return False

def shift_boxes(grid, r_ahead, c_ahead, rx, cx):
    box_in_the_way = False
    while True:
        if grid[r_ahead][c_ahead] == BOX:
            box_in_the_way = True
            r_ahead += rx
            c_ahead += cx
        else:
            break

    if box_in_the_way:
        grid[r_ahead][c_ahead] = BOX

def do_move(grid, r, c, direction):
    grid[r][c] = EMPTY

    rx, cx = get_step_for_direction(direction)
    r += rx
    c += cx
    shift_boxes(grid, r, c, rx, cx)

    grid[r][c] = ROBOT
    return r, c


def move_robot(grid, r, c, direction):
    if can_move(gather_line_ahead(grid, r, c, direction)):
        return do_move(grid, r, c, direction)
    return r, c

def print_grid(grid):
    for row in grid:
        print("".join(row))

def calc_gps(grid):
    gps = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == BOX:
                gps += 100 * r + c

    return gps

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        first, second = file.read().split("\n\n")
        grid = [list(line.strip()) for line in first.split()]
        moves = "".join(second.split())

    r, c = find_robot(grid)
    for direction in moves:
        r, c = move_robot(grid, r, c, direction)
    print_grid(grid)

    print(calc_gps(grid))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-15")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
