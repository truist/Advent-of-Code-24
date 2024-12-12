#!/usr/bin/env python3

"""
Advent of Code 2024-11
"""

import argparse

def do_blink(stones):
    i = 0;
    while True:
        cur_val = stones[i]
        if cur_val == 0:
            stones[i] = 1
        elif len(str(cur_val)) % 2 == 0:
            str_val = str(cur_val)
            half_len = len(str_val) // 2
            left, right = str_val[:half_len], str_val[half_len:]
            stones[i] = int(left)
            stones.insert(i + 1, int(right))
            i += 1
        else:
            stones[i] = cur_val * 2024

        i += 1
        if i == len(stones):
            break

def main(inputfile, blinks):
    with open(inputfile, 'r', encoding='utf-8') as file:
        stones = [int(val) for val in file.read().split()]

    for blink in range(blinks):
        # print(stones)
        do_blink(stones)

    print(len(stones))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-11")
    parser.add_argument("input", help="input data file")
    parser.add_argument("blinks", type=int, help="number of times to blink")

    args = parser.parse_args()
    main(args.input, args.blinks)
