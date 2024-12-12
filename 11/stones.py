#!/usr/bin/env python3

"""
Advent of Code 2024-11
"""

import argparse

cache = {}

def do_blinks(cur_val, blinks):
    if blinks == 0:
        return 1

    if cur_val == 0:
        return cache_blinks(1, blinks - 1)

    if len(str(cur_val)) % 2 == 0:
        str_val = str(cur_val)
        half_len = len(str_val) // 2
        left, right = str_val[:half_len], str_val[half_len:]
        return cache_blinks(int(left), blinks - 1) + cache_blinks(int(right), blinks - 1)

    return cache_blinks(cur_val * 2024, blinks - 1)

def cache_blinks(cur_val, blinks):
    key = (cur_val, blinks)
    if key in cache:
        return cache[key]

    answer = do_blinks(cur_val, blinks)
    cache[key] = answer

    return answer

def main(inputfile, blinks):
    with open(inputfile, 'r', encoding='utf-8') as file:
        stones = [int(val) for val in file.read().split()]

    total = 0
    for stone in stones:
        total += do_blinks(stone, blinks)

    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-11")
    parser.add_argument("input", help="input data file")
    parser.add_argument("blinks", type=int, help="number of times to blink")

    args = parser.parse_args()
    main(args.input, args.blinks)
