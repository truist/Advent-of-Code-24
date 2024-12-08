#!/usr/bin/env python3

"""
Advent of Code 2024-05
"""

import argparse

def fix_one_invalid(each, rules):
    """
    do one pass through the rules, swapping bad pairs
    """
    for rule in rules:
        try:
            left = each.index(rule[0])
            right = each.index(rule[1])
            if right < left:
                # just swap them
                right_val = each[right]
                each[right] = each[left]
                each[left] = right_val
        except ValueError:
            pass # this rule doesn't apply; just try the next one

def fix_all_invalid(invalid, rules):
    """
    fix all the invalid prints
    """
    for each in invalid:
        while True:
            fix_one_invalid(each, rules)
            if check_print(each, rules):
                break

def check_print(each, rules):
    """
    check a single print to see if it meets all the rules
    """
    for rule in rules:
        try:
            left = each.index(rule[0])
            right = each.index(rule[1])
            if right < left:
                return False
        except ValueError:
            pass # this rule doesn't apply; just try the next one

    return True

def find_valid_prints(prints, rules):
    """
    check each print to see if it meets all the rules
    """
    valid = []
    invalid = []
    for each in prints:
        if check_print(each, rules):
            valid += [each]
        else:
            invalid += [each]

    return (valid, invalid)

def main(inputfile):
    """
    Process the input data
    """
    rules = []
    prints = []
    in_rules = True
    with open(inputfile, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "" == line:
                in_rules = False
                continue
            if in_rules:
                rules += [line.split("|")]
            else:
                prints += [line.split(",")]

    (valid, invalid) = find_valid_prints(prints, rules)
    print(sum(int(each[len(each) // 2]) for each in valid))

    fix_all_invalid(invalid, rules)
    print(sum(int(each[len(each) // 2]) for each in invalid))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-05")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
