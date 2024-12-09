#!/usr/bin/env python3

"""
Advent of Code 2024-09
"""

import argparse
from dataclasses import dataclass

@dataclass
class Record:
    id: int
    size: int

def convert_dense_to_records(dense):
    records = []
    next_id = 0
    in_file = True
    for size in dense:
        if in_file:
            records += [Record(next_id, size)]
            next_id += 1
        else:
            records += [Record(-1, size)]
        in_file = not in_file

    return records

def bring_forward(records, to_bring, empty_location):
    popped = records.pop(to_bring)
    records.insert(to_bring, Record(-1, popped.size))

    records.insert(empty_location, popped)

    if records[empty_location + 1].size == popped.size:
        records.pop(empty_location + 1)
        return 0

    records[empty_location + 1].size -= popped.size
    return 1

def defrag(records):
    cur_end = len(records) - 1
    while True:
        inserted = 0
        if records[cur_end].id != -1:
            for cur_beg in range(cur_end):
                if records[cur_beg].id == -1 and records[cur_beg].size >= records[cur_end].size:
                    inserted += bring_forward(records, cur_end, cur_beg)
                    break

        cur_end -= (1 - inserted)
        if cur_end == 0:
            break

    return records

def calc_checksum(records):
    checksum = 0
    block_position = 0
    for record in records:
        for _ in range(record.size):
            if record.id > -1:
                checksum += block_position * record.id
            block_position += 1

    return checksum

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        dense = [int(record) for record in list(file.read().strip())]
    # print(dense)

    records = convert_dense_to_records(dense)
    # print(records)

    defrag(records)
    # print(records)

    print(calc_checksum(records))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-09")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
