#!/usr/bin/env python3

"""
Advent of Code 2024-19
"""

import argparse

def count_ways(pattern, towels, cache):
    if len(pattern) == 0:
        return 1

    if pattern in cache:
        return cache[pattern]

    ways = 0
    for towel in towels:
        if pattern.startswith(towel):
            new_start = len(towel)
            sub_pattern = pattern[new_start:]
            new_ways = count_ways(sub_pattern, towels, cache)
            if new_ways > 0:
                cache[sub_pattern] = new_ways
                ways += new_ways

    return ways

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        towels, patterns = file.read().split("\n\n")
        towels = [towel.strip() for towel in towels.split(",")]
        patterns = patterns.strip().split("\n")

    ways = 0
    cache = {}
    for pattern in patterns:
        # print(f"testing {pattern}")
        ways += count_ways(pattern, towels, cache)

    print(ways)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-19")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
