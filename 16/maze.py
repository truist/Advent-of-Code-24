#!/usr/bin/env python3

"""
Advent of Code 2024-16
"""

import argparse
from dataclasses import dataclass

N = 0
E = 1
S = 2
W = 3

UNKNOWN = -1
LOOP_DETECTION = -2
WALL = -3
DEAD_END = 1000000000

@dataclass
class Node:
    grid: list
    r: int
    c: int
    val: str
    no_turn_costs: list
    best_direction: int

    def neighbor(self, direction):
        if direction == N:
            return self.grid[self.r - 1][self.c]
        if direction == E:
            return self.grid[self.r][self.c + 1]
        if direction == S:
            return self.grid[self.r + 1][self.c]
        if direction == W:
            return self.grid[self.r][self.c - 1]
        raise ValueError(f"Unknown direction: {direction}")

    def print(self):
        return f"({self.r},{self.c}): {self.val}; {self.no_turn_costs} / {self.best_direction}"

    def debug(self, message, heading, steps_so_far):
        if self.r == 5 and 1 <= self.c <= 3:
            print(f"[{self.r},{self.c},{heading}]: {message} ### {self.print()}")
            stepline = []
            for step in steps_so_far:
                if step[0] == 5 and 1 <= step[1] <= 3:
                    stepline.append(f"[{step[0]},{step[1]},{step[2]}]")
            # print("  ", "".join(stepline))

    def non_backwards(self, heading):
        for new_dir in [N, E, S, W]:
            if (heading + 2) % 4 == new_dir: # don't go backwards
                continue
            yield new_dir, self.neighbor(new_dir)

    def turn_cost(self, heading, want_to_go):
        return 0 if heading == want_to_go else 1000

    def find_cheapest_direction(self, heading, steps_so_far):
        # self.debug("Entering find_cheapest_direction", heading)
        best_direction = (-1, -1)
        for new_dir, next_step in self.non_backwards(heading):
            next_step_cost = next_step.find_cheapest_path(new_dir, steps_so_far)
            if next_step_cost > -1:
                if best_direction[1] == -1 or next_step_cost < best_direction[1]:
                    best_direction = (new_dir, next_step_cost)
            elif next_step_cost == LOOP_DETECTION and best_direction[0] == -1:
                best_direction = (-1, LOOP_DETECTION)

        self.debug(f"Found best direction: {best_direction}", heading, steps_so_far)
        return best_direction

    def find_cheapest_path(self, heading, steps_so_far):
        """
        find the cheapest path to the end, for the case where you moved
        into this node while traveling in {heading}
        """
        self.debug("Entering find_cheapest_path", heading, steps_so_far)
        if self.val == "E":
            return 0
        if self.val == "#":
            return WALL
        if self.no_turn_costs[heading] > 0:
            self.debug("Returning cached cost", heading, steps_so_far)
            return self.no_turn_costs[heading] + self.turn_cost(heading, self.best_direction)

        current_step = (self.r, self.c, heading)
        if current_step in steps_so_far:
            self.debug("Loop detected", heading, steps_so_far)
            return LOOP_DETECTION
        steps_so_far.append(current_step)

        # if self.no_turn_costs[heading] == LOOP_DETECTION:
        #     self.debug("Loop detected", heading)
        #     return LOOP_DETECTION
        # self.no_turn_costs[heading] = LOOP_DETECTION

        best_direction, best_cost = self.find_cheapest_direction(heading, steps_so_far)
        if best_cost == LOOP_DETECTION:
            return LOOP_DETECTION
        if best_cost < 0:
            self.no_turn_costs[heading] = DEAD_END
            self.debug("Dead end", heading, steps_so_far)
            return DEAD_END

        self.best_direction = best_direction
        self.no_turn_costs[heading] = best_cost + 1
        self.debug("Returning from find_cheapest_path", heading, steps_so_far)
        return self.no_turn_costs[heading] + self.turn_cost(heading, best_direction)

    def print_cheapest_path(self):
        print(self.print())

        if self.val != "E":
            self.neighbor(self.best_direction).print_cheapest_path()

def convert_grid_to_nodes(grid):
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            grid[r][c] = Node(grid, r, c, val, [UNKNOWN, UNKNOWN, UNKNOWN, UNKNOWN], -1)

def print_grid(grid):
    printable_row = []
    for _, row in enumerate(grid):
        for node in row:
            printable_row.append(f"{node.r},{node.c},{node.val}")
        print(" ".join(printable_row))

def find_start_point(grid):
    r = len(grid) - 2
    c = 1
    node = grid[r][c]
    if node.val != "S":
        raise ValueError(f"Start point is not where expected: {node}")

    return node

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    convert_grid_to_nodes(grid)
    # print_grid(grid)

    start_node = find_start_point(grid)
    print(start_node.find_cheapest_path(E, []))

    start_node.print_cheapest_path()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-16")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
