#!/usr/bin/env python3

"""
Advent of Code 2024-16
"""

import argparse
import heapq

OFFSETS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIRECTIONS = ["N", "E", "S", "W"]

def debug(position, message):
    if False and position[0] == 1:
        print(message)

def neighbors(grid, position):
    for i, (dr, dc) in enumerate(OFFSETS):
        nr, nc = position[0] + dr, position[1] + dc
        if grid[nr][nc] != "#":
            yield (nr, nc, DIRECTIONS[i])

# A* search courtesy of ChatGPT
def find_cheapest_path(grid, start_position, start_direction):
    heap = [(0, start_position, start_direction, [start_position])]
    visited = set()

    while heap:
        cost, position, direction, path = heapq.heappop(heap)

        if position in visited:
            continue
        visited.add(position)

        val = grid[position[0]][position[1]]
        debug(position, f"Evaluating position {position} at {cost} with value {val}")
        if val == "E":
            return cost, path

        for neighbor in neighbors(grid, position):
            new_position, new_direction = neighbor[:2], neighbor[2]
            if direction != new_direction:
                new_cost = cost + 1001
            else:
                new_cost = cost + 1

            debug(position, f"pushing {new_position} heading {new_direction} at {new_cost} onto heap")
            heapq.heappush(
                heap,
                (new_cost, new_position, new_direction, path + [new_position])
            )

    raise ValueError("Could not find a path!")

def print_path(grid, path):
    for r, row in enumerate(grid):
        rowstr = []
        for c, val in enumerate(row):
            if (r, c) in path:
                val = "*"
            rowstr.append(val)
        print("".join(rowstr))

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    start_node = (len(grid) - 2, 1)
    cost, path = find_cheapest_path(grid, start_node, "E")
    print(cost)
    # print_path(grid, path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-16")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
