#!/usr/bin/env python3

"""
Advent of Code 2024-20
"""

import argparse
from dataclasses import dataclass
from collections import deque

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

STEPS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

@dataclass
class Cell:
    r: int
    c: int
    val: str
    dist: int
    grid: list

def convert_grid(grid):
    start = None
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            cell = Cell(r, c, val, -1, grid)
            grid[r][c] = cell
            if val == START:
                start = cell

    return start

def neighbors(grid, cell, dist):
    for step in STEPS:
        new_r = cell.r + step[0] * dist
        new_c = cell.c + step[1] * dist

        if 0 <= new_r < len(grid) and 0 <= new_c < len(grid[0]):
            neighbor = grid[new_r][new_c]
            if neighbor.val != WALL:
                yield neighbor

def map_distances(grid, start):
    queue = deque([start])
    visited = set()
    visited.add((start.r, start.c))
    start.dist = 0

    path = []
    while queue:
        current_cell = queue.popleft()
        path.append(current_cell)
        for neighbor in neighbors(grid, current_cell, 1):
            position = (neighbor.r, neighbor.c)
            if position not in visited:
                visited.add(position)
                neighbor.dist = current_cell.dist + 1
                queue.append(neighbor)

    return path

def print_grid(grid):
    for row in grid:
        printable = []
        for cell in row:
            if cell.val == EMPTY:
                printable.append(f"{cell.dist:<2}")
            else:
                printable.append(cell.val)
                printable.append(" ")
        print("".join(printable))

def find_shortcuts(grid, path, min_savings):
    shortcuts = set()
    for current_cell in path:
        for jump in neighbors(grid, current_cell, 2):
            if jump.dist - current_cell.dist - 2 >= min_savings:
                shortcuts.add((current_cell.r, current_cell.c, jump.r, jump.c))

    return shortcuts

def main(inputfile, min_savings):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]
    # print(grid)

    start = convert_grid(grid)
    path = map_distances(grid, start)
    # print_grid(grid)
    print(len(path))

    shortcuts = find_shortcuts(grid, path, min_savings)
    # print(shortcuts)
    print(len(shortcuts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-20")
    parser.add_argument("input", help="input data file")
    parser.add_argument("min_savings", type=int, help="minimum shortcut to count")

    args = parser.parse_args()
    main(args.input, args.min_savings)
