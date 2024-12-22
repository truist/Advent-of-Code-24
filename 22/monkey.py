#!/usr/bin/env python3

"""
Advent of Code 2024-22
"""

import argparse

SEQ_LEN = 4

all_sequences = {}
def update_all_sequences(sequence, price):
    if sequence not in all_sequences:
        all_sequences[sequence] = price
    else:
        all_sequences[sequence] += price

class Buyer:
    def __init__(self):
        self.secrets = []
        self.prices = []
        self.deltas = []

        self.sequence_cache = {}

    def append(self, secret, last_price):
        self.secrets.append(secret)

        price = secret % 10
        self.prices.append(price)

        if last_price is not None:
            self.deltas.append(price - last_price)
        else:
            self.deltas.append(None)

        if len(self.deltas) > SEQ_LEN:
            sequence = tuple(self.deltas[-SEQ_LEN:])
            if sequence not in self.sequence_cache:
                self.sequence_cache[sequence] = price
                update_all_sequences(sequence, price)

        return price

def prune_mix(secret, modified):
    return (modified ^ secret) % 16777216

def iterate(secret, count):
    buyer = Buyer()

    last_price = buyer.append(secret, None)
    for _ in range(count):
        secret = prune_mix(secret * 64, secret)
        secret = prune_mix(secret // 32, secret)
        secret = prune_mix(secret * 2048, secret)

        last_price = buyer.append(secret, last_price)

def find_optimal_sequence():
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

    for seed in buyer_seeds:
        iterate(seed, 2000)

    sequence, total = find_optimal_sequence()
    print(sequence)
    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-22")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
