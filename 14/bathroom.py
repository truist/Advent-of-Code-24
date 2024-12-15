#!/usr/bin/env python3

"""
Advent of Code 2024-14
"""

import argparse
from dataclasses import dataclass

@dataclass
class Robot:
    x: int
    y: int
    dx: int
    dy: int

    def move(self, time, width, height):
        for _ in range(time):
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

def main(inputfile, width, height):
    robots = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            robots.append(parse_line(line))

    for robot in robots:
        robot.move(100, width, height)

    print(safety_factor(robots, width // 2, height // 2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-14")
    parser.add_argument("input", help="input data file")
    parser.add_argument("width", type=int, help="input data file")
    parser.add_argument("height", type=int, help="input data file")

    args = parser.parse_args()
    main(args.input, args.width, args.height)
