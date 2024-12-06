#!/usr/bin/env python3

"""
Advent of Code 2024-02
"""

import argparse

def safe(report, error_count):
    """
    Calculate whether a report is safe
    """
    if len(report) < 2:
        # only 1 report; let's assume that counts as safe
        return True

    increasing = report[1] > report[0]
    if error_count < 1 and len(report) > 2:
        second_increasing = report[2] > report[1]
        if second_increasing != increasing:
            # it would have been better to just brute force all the permutations
            remove_0 = report[1:]
            remove_1 = [report[0]] + report[2:]
            remove_2 = report[:2] + report[3:]
            result = safe(remove_0, 1) or safe(remove_1, 1) or safe(remove_2, 1)
            # print(f"{"safe" if result else "unsafe"}: {report}")
            return result

    last_level = report[0]
    for index, level in enumerate(report[1:]):
        diff = abs(level - last_level)
        if (level > last_level) != increasing or diff < 1 or diff > 3:
            if error_count == 0:
                index += 1 # to account for the '1:' when we started this loop
                remove_prior = report[:index - 1] + report[index:]
                remove_current = report[:index] + report[index + 1:]
                result = safe(remove_prior, 1) or safe(remove_current, 1)
                # print(f"{"safe" if result else "unsafe"}: {report}")
                return result

            return False

        last_level = level

    return True


def main(inputfile):
    """
    Process the input data
    """
    reports = []
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            reports.append([int(strint) for strint in line.split()])

    totalsafe = 0
    for report in reports:
        result = safe(report, 0)
        # if not result:
        #     print(report)
        totalsafe += 1 if result else 0

    print(f"Total safe: {totalsafe}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-02")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
