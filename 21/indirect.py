#!/usr/bin/env python3

"""
Advent of Code 2024-21
"""

import argparse

nkp = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
    "O": (3, 0), "0": (3, 1), "A": (3, 2),
}

dkp = {
    "O": (0, 0), "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2)
}

def add_path(dd, neg, pos):
    return (neg if dd < 0 else pos) * abs(dd)

def get_path_between(start_char, end_char, keypad):
    start_pos = keypad[start_char]
    end_pos = keypad[end_char]

    dr = end_pos[0] - start_pos[0]
    dc = end_pos[1] - start_pos[1]

    rows_first = False
    cols_first = False
    avoid = keypad["O"]
    if start_pos[0] == avoid[0] and end_pos[1] == avoid[1]:
        rows_first = True
    elif start_pos[1] == avoid[1] and end_pos[0] == avoid[0]:
        cols_first = True

    path = ""
    if rows_first:
        path += add_path(dr, "^", "v")
        path += add_path(dc, "<", ">")
    elif cols_first:
        path += add_path(dc, "<", ">")
        path += add_path(dr, "^", "v")
    else:
        # order matters here, for indirect distance optimization
        if dc < 0:
            path += "<" * -dc
        if dr > 0:
            path += "v" * dr
        if dr < 0:
            path += "^" * -dr
        if dc > 0:
            path += ">" * dc

    return path

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        codes = [line.strip() for line in file]
    # print(codes)

    keypads = [nkp, dkp, dkp]

    complexity = 0
    for code in codes:
        simpler_str = code
        for keypad in keypads:
            print(simpler_str)
            indirect_str = ""
            last_char = "A"
            for char in simpler_str:
                indirect_str += get_path_between(last_char, char, keypad) + "A"
                last_char = char
            simpler_str = indirect_str
        print(indirect_str)

        print(len(indirect_str), int(code[0:-1]))
        complexity += len(indirect_str) * int(code[0:-1])
        print()
    print(complexity)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-21")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
