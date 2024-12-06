#!/usr/bin/env python3

"""
Advent of Code 2024-01
"""

import argparse

def similarity(left, right):
    """
    Calculate the similarity between the two lists
    """
    simil=0
    for l in left:
        simil += l * right.count(l)

    print(f"Total similarity: {simil}")

def distance(left, right):
    """
    Calculate the distance between the two lists
    """
    dist = 0
    for l, r in zip(left, right):
        dist += abs(r - l)

    print(f"Total distance: {dist}")

def main(inputfile):
    """
    Process the input data
    """

    left = []
    right = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            (l, r) = line.split()
            left.append(int(l))
            right.append(int(r))

    left.sort()
    right.sort()

    distance(left, right)
    similarity(left, right)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-01")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
