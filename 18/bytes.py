#!/usr/bin/env python3

"""
Advent of Code 2024-18
"""

import argparse
from collections import deque

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def find_shortest_path(rows, cols, walls):
    queue = deque([(0, 0, 0)])
    visited = set()
    visited.add((0, 0))

    while queue:
        r, c, dist = queue.popleft()
        if r == rows - 1 and c == cols - 1:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_spot = (nr, nc)
                if new_spot not in walls and new_spot not in visited:
                    visited.add(new_spot)
                    queue.append((nr, nc, dist + 1))

    return -1

def main(inputfile, width, height, time):
    byte_coords = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            x, y = line.split(",")
            byte_coords.append((int(y), int(x))) # swap x and y for r and c
    # print(byte_coords)

    print(find_shortest_path(width, height, byte_coords[0:time]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-18")
    parser.add_argument("input", help="input data file")
    parser.add_argument("width", type=int, help="input data file")
    parser.add_argument("height", type=int, help="input data file")
    parser.add_argument("time", type=int, help="input data file")

    args = parser.parse_args()
    main(args.input, args.width, args.height, args.time)
