#!/usr/bin/env python3

"""
Advent of Code 2024-16
"""

import argparse
import heapq
from collections import defaultdict

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
def find_all_paths(grid, start_position, start_direction):
    heap = [(0, start_position, start_direction, [start_position])]
    visited = defaultdict(lambda: float('inf'))
    min_cost = float('inf')

    while heap:
        cost, position, direction, path = heapq.heappop(heap)

        if cost > min_cost:
            continue

        val = grid[position[0]][position[1]]
        debug(position, f"Evaluating position {position} at {cost} with value {val}")
        if val == "E":
            debug(position, "found the end")
            if cost < min_cost:
                min_cost = cost
                yield (cost, path)
            elif cost == min_cost:
                yield (cost, path)
            else:
                continue

        if visited[(position, direction)] < cost:
            continue
        visited[(position, direction)] = cost

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

def find_all_cheapest_paths(grid, start_position, start_direction):
    paths = defaultdict(lambda: [])
    for cost, path in find_all_paths(grid, start_position, start_direction):
        paths[cost].append(path)

    all_nodes = set()
    min_cost = min(list(paths))
    print(f"min cost is {min_cost} with {len(paths[min_cost])} paths")
    for path in paths[min_cost]:
        all_nodes.update(path)
    return len(all_nodes)

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

    cost = find_all_cheapest_paths(grid, (len(grid) - 2, 1), "E")
    print(cost)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-16")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
