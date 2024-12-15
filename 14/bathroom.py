#!/usr/bin/env python3

"""
Advent of Code 2024-14
"""

import argparse
import time
from dataclasses import dataclass

@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def move(self, steps, width, height):
        for _ in range(steps):
            self.x += self.dx
            self.y += self.dy
        self.x %= width
        self.y %= height
        if self.x < 0:
            self.x += width
        if self.y < 0:
            self.y += height


def extract_values(line_part):
    _, values = line_part.split("=")
    x, y = values.split(",")
    return int(x), int(y)

def parse_line(line):
    p, v = line.split()
    x, y = extract_values(p)
    dx, dy = extract_values(v)
    return Robot(x, y, dx, dy)

def safety_factor(robots, mid_width, mid_height):
    nw = 0
    ne = 0
    se = 0
    sw = 0
    for robot in robots:
        if robot.x < mid_width:
            if robot.y < mid_height:
                nw += 1
            elif robot.y > mid_height:
                sw += 1
        elif robot.x > mid_width:
            if robot.y < mid_height:
                ne += 1
            elif robot.y > mid_height:
                se += 1

    # print(nw, ne, se, sw)
    return nw * ne * se * sw

def print_grid(robots, width, height):
    grid = []
    for _ in range(height):
        row = []
        grid.append(row)
        for _ in range(width):
            row.append(".")

    for robot in robots:
        if grid[robot.y][robot.x] == ".":
            grid[robot.y][robot.x] = "1"
        else:
            grid[robot.y][robot.x] = str(int(grid[robot.y][robot.x]) + 1)

    for row in grid:
        print("".join(row))

def take_steps(robots, steps, width, height):
    for robot in robots:
        robot.move(steps, width, height)
    return steps

def main(inputfile, width, height):
    robots = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            robots.append(parse_line(line))

    total_steps = 0
    for _ in range(10000):
        total_steps += take_steps(robots, 1, width, height)
        sf = safety_factor(robots, width // 2, height // 2)
        if sf <= 84543414:
            print(total_steps, sf)
            print_grid(robots, width, height)

    print(safety_factor(robots, width // 2, height // 2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-14")
    parser.add_argument("input", help="input data file")
    parser.add_argument("width", type=int, help="input data file")
    parser.add_argument("height", type=int, help="input data file")

    args = parser.parse_args()
    main(args.input, args.width, args.height)
