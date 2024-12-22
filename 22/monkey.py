#!/usr/bin/env python3

"""
Advent of Code 2024-22
"""

import argparse

def mix(result, number):
    return result ^ number

def prune(number):
    return number % 16777216

def iterate(number, count):
    for _ in range(count):
        number = prune(mix(number * 64, number))
        number = prune(mix(number // 32, number))
        number = prune(mix(number * 2048, number))
    return number

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        seeds = [int(line.strip()) for line in file]
    # print(seeds)

    total = 0
    for seed in seeds:
        total += iterate(seed, 2000)

    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-22")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
