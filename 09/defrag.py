#!/usr/bin/env python3

"""
Advent of Code 2024-09
"""

import argparse

def expand_map(records):
    disk_map = []
    next_id = 0
    in_file = True
    for record in records:
        for _ in range(record):
            disk_map += [next_id if in_file else -1]
        if in_file:
            next_id += 1
        in_file = not in_file

    return disk_map

def find_next_file(disk_map, offset):
    if disk_map[offset] != -1:
        return offset

    return find_next_file(disk_map, offset - 1)

def defrag(disk_map):
    checksum = 0

    file_end = find_next_file(disk_map, -1)
    for i, block in enumerate(disk_map):
        if block == -1:
            disk_map[i] = disk_map[file_end]
            disk_map[file_end] = -1
            file_end = find_next_file(disk_map, file_end - 1)

        checksum += i * disk_map[i]

        if i == len(disk_map) + file_end:
            break

    return checksum


def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        records = [int(record) for record in list(file.read().strip())]
    # print(records)

    disk_map = expand_map(records)
    # print(disk_map)

    print(defrag(disk_map))
    # print(disk_map)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-09")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
