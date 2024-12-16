#!/usr/bin/env python3

"""
Advent of Code 2024-15
"""

import argparse
import time
from dataclasses import dataclass

ROBOT = "@"
SMALL_BOX = "O"
BOX_LEFT = "["
BOX_RIGHT = "]"
WALL = "#"
EMPTY = "."
N = "^"
E = ">"
S = "v"
W = "<"

@dataclass
class Box:
    row: int
    left: int
    right: int

def widen_grid(grid):
    wide_grid = []
    for row in grid:
        wide_row = []
        wide_grid.append(wide_row)
        for val in row:
            if val == ROBOT:
                new_cell = (ROBOT, EMPTY)
            elif val == SMALL_BOX:
                new_cell = (BOX_LEFT, BOX_RIGHT)
            elif val == WALL:
                new_cell = (WALL, WALL)
            elif val == EMPTY:
                new_cell = (EMPTY, EMPTY)
            else:
                raise ValueError(f"Unknown cell value: {val}")

            wide_row += [*new_cell]

    return wide_grid

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

def walk_line_ahead(grid, r, c, direction):
    rx, cx = get_step_for_direction(direction)
    r += rx
    c += cx

    while 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        yield r, c
        r += rx
        c += cx

def can_move(grid, r, c, direction):
    for r_ahead, c_ahead in walk_line_ahead(grid, r, c, direction):
        cell = grid[r_ahead][c_ahead]
        if cell == WALL:
            return False
        if cell == EMPTY:
            return True
        if direction in [N, S]:
            if cell == BOX_LEFT:
                if not can_move(grid, r_ahead, c_ahead + 1, direction):
                    return False
            if cell == BOX_RIGHT:
                if not can_move(grid, r_ahead, c_ahead - 1, direction):
                    return False
    return False


def shift_boxes_ew(grid, r, c, cx):
    last_box = -1
    moving_w = cx < 0
    for c_ahead in range(c, 0 if moving_w else len(grid[0]), -1 if moving_w else 1):
        if grid[r][c_ahead] in [BOX_LEFT, BOX_RIGHT]:
            last_box = c_ahead
        else:
            break

    if last_box != -1:
        for c_ahead in range(last_box, c, 2 if moving_w else -2):
            if cx < 0:
                grid[r][c_ahead - 1] = BOX_LEFT
                grid[r][c_ahead] = BOX_RIGHT
            else:
                grid[r][c_ahead + 1] = BOX_RIGHT
                grid[r][c_ahead] = BOX_LEFT
        return True
    return False

def find_boxes_in_row(grid, row, left, right):
    box_lists = []
    current_list = []

    col = left
    blank_spaces = 0
    while col <= right:
        if blank_spaces == 2 and len(current_list) > 0:
            box_lists.append(current_list)
            current_list = []
        if grid[row][col] == BOX_LEFT:
            current_list.append(Box(row, col, col + 1))
            col += 2
            blank_spaces = 0
        else:
            col += 1
            blank_spaces += 1

    if len(current_list) > 0:
        box_lists.append(current_list)

    return box_lists

def shift_box_list_ns(grid, box_list, rx):
    # print(f"shifting: {box_list}, {rx}")
    current_row = box_list[0].row
    current_left_edge = box_list[0].left
    current_right_edge = box_list[-1].right

    next_row = current_row + rx
    next_left_edge = current_left_edge
    next_right_edge = current_right_edge
    if grid[next_row][current_left_edge] == BOX_RIGHT:
        next_left_edge -= 1
    if grid[next_row][current_right_edge] == BOX_LEFT:
        next_right_edge += 1

    next_box_lists = find_boxes_in_row(grid, next_row, next_left_edge, next_right_edge)
    if len(next_box_lists) > 0:
        for current_list in next_box_lists:
            shift_box_list_ns(grid, current_list, rx)

    for col in range(current_left_edge, current_right_edge + 1):
        # print(f"moving {current_row},{col} to {next_row},{col}")
        grid[next_row][col] = grid[current_row][col]
        grid[current_row][col] = EMPTY

def shift_boxes_ns(grid, r, c, rx):
    cell = grid[r][c]
    if cell == BOX_LEFT:
        shift_box_list_ns(grid, [Box(r, c, c + 1)], rx)
        grid[r][c + 1] = EMPTY
        return True
    if cell == BOX_RIGHT:
        shift_box_list_ns(grid, [Box(r, c - 1, c)], rx)
        grid[r][c - 1] = EMPTY
        return True
    return False

def shift_boxes(grid, r, c, rx, cx):
    if cx != 0:
        return shift_boxes_ew(grid, r, c, cx)
    return shift_boxes_ns(grid, r, c, rx)

def do_move(grid, r, c, direction):
    grid[r][c] = EMPTY

    rx, cx = get_step_for_direction(direction)
    r += rx
    c += cx
    shifted = shift_boxes(grid, r, c, rx, cx)

    grid[r][c] = ROBOT
    return r, c, shifted

def move_robot(grid, r, c, direction):
    if can_move(grid, r, c, direction):
        return do_move(grid, r, c, direction)
    return r, c, True

def print_grid(grid):
    for row in grid:
        print("".join(row))

def print_grid_segment(grid, r, c, direction, replace_robot_with_direction):
    buffer = 7
    # print(f"r: {r}")
    for current_r in range(max(0, r - buffer), min(r + buffer + 1, len(grid))):
        c_min = max(0, c - buffer * 2)
        c_max = min(c + buffer * 2 + 1, len(grid[0]))
        cells = grid[current_r][c_min:c_max]
        if replace_robot_with_direction and current_r == r:
            cells[buffer * 2] = direction
        print("".join(cells))

def calc_gps(grid):
    gps = 0
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == BOX_LEFT:
                gps += 100 * r + c

    return gps

def animate(grid, r, c, direction, last_direction, interesting, step):
    # clear the screen
    if not 3104 <= step <= 3106:
        print("\033[2J\033[H", end="")
    print_grid_segment(grid, r, c, last_direction, True)
    # print("")
    # print_grid_segment(grid, 11, 45, last_direction, False)
    print(f"next move is {direction} step {step}")
    print(f"current position is {r},{c}")
    if step > 4930:
        if 1898 <= step < 1905:
            time.sleep(4)
        elif 3104 <= step <= 3106:
            time.sleep(4)
        elif 3145 <= step <= 3155:
            time.sleep(4)
        elif 4940 <= step <= 4945:
            time.sleep(4)
        elif interesting:
            time.sleep(.1)
        else:
            time.sleep(0.01)

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        first, second = file.read().split("\n\n")
        grid = [list(line.strip()) for line in first.split()]
        moves = "".join(second.split())

    grid = widen_grid(grid)
    # print_grid(grid)
    r, c = find_robot(grid)

    interesting = False
    step = 0
    last_direction = "@"
    for direction in moves:
        # animate(grid, r, c, direction, last_direction, interesting, step)

        r, c, interesting = move_robot(grid, r, c, direction)

        last_direction = direction
        step += 1

    print_grid(grid)

    print(calc_gps(grid))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-15")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
