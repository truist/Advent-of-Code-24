#!/usr/bin/env python3

"""
Advent of Code 2024-23
"""

import argparse
from dataclasses import dataclass
from itertools import combinations

@dataclass
class Computer:
    name: str
    connected: dict

    def pair(self, other):
        if other.name not in self.connected:
            self.connected[other.name] = other

def add_computer(name, computers):
    if name not in computers:
        computers[name] = Computer(name, {})
    return computers[name]

def pair_up(pairings):
    computers = {}
    for pairing in pairings:
        left, right = pairing.split("-")
        left = add_computer(left, computers)
        right = add_computer(right, computers)
        left.pair(right)
        right.pair(left)
    return computers

def intersection(left, right):
    return list(sorted(set(left) & set(right)))

def full_list(computer):
    return [computer.name]+ list(computer.connected.keys())

def find_fully_connected(subset, computers):
    fully_connected = subset
    for name in subset[2:]:
        fully_connected = intersection(fully_connected, full_list(computers[name]))
    return fully_connected

def add_fully_connected(candidates, groups, computers):
    if tuple(candidates) in groups:
        return

    fully_connected = find_fully_connected(candidates, computers)
    groups.add(tuple(fully_connected))

def find_groups(computers):
    groups = set()
    for computer in computers.values():
        for partner in computer.connected.values():
            candidates = intersection(full_list(computer), full_list(partner))
            add_fully_connected(candidates, groups, computers)

    return groups

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        pairings = [line.strip() for line in file]
    # print(pairings)

    computers = pair_up(pairings)
    groups = find_groups(computers)

    max_len = 0
    longest_group = tuple()
    for group in groups:
        if len(group) > max_len:
            max_len = len(group)
            longest_group = group

    print(",".join(list(longest_group)))
    # print(len(groups))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-23")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
