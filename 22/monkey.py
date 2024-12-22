#!/usr/bin/env python3

"""
Advent of Code 2024-22
"""

import argparse

SEQ_LEN = 4

def prune_mix(secret, modified):
    return (modified ^ secret) % 16777216

def append(secret, last_price, deltas, only_first_sequences, all_sequences):
    price = secret % 10

    if last_price is not None:
        deltas.append(price - last_price)
    else:
        deltas.append(None)

    if len(deltas) > SEQ_LEN:
        sequence = tuple(deltas[-SEQ_LEN:])
        if sequence not in only_first_sequences:
            only_first_sequences.add(sequence)

            if sequence not in all_sequences:
                all_sequences[sequence] = price
            else:
                all_sequences[sequence] += price

    return price

def iterate(secret, count, all_sequences):
    deltas = []
    only_first_sequences = set()

    last_price = append(secret, None, deltas, only_first_sequences, all_sequences)
    for _ in range(count):
        secret = prune_mix(secret * 64, secret)
        secret = prune_mix(secret // 32, secret)
        secret = prune_mix(secret * 2048, secret)

        last_price = append(secret, last_price, deltas, only_first_sequences, all_sequences)

def find_optimal_sequence(all_sequences):
    max_price = 0
    best_sequence = None
    for sequence, price in all_sequences.items():
        if price > max_price:
            print(f"new max price: {price} with sequence {sequence}")
            max_price = price
            best_sequence = sequence

    return best_sequence, max_price

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        buyer_seeds = [int(line.strip()) for line in file]

    all_sequences = {}
    for seed in buyer_seeds:
        iterate(seed, 2000, all_sequences)

    sequence, total = find_optimal_sequence(all_sequences)
    print(sequence)
    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-22")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
