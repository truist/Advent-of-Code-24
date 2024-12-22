#!/usr/bin/env python3

"""
Advent of Code 2024-22
"""

import argparse
from dataclasses import dataclass

SEQ_LEN = 4

class Buyer:
    def __init__(self):
        self.secrets = []
        self.prices = []
        self.deltas = []

        self.max_price = -1
        self.sequence_cache = {}

    def append(self, secret, last_price):
        self.secrets.append(secret)

        price = secret % 10
        self.prices.append(price)
        self.max_price = max(self.max_price, price)

        if last_price is not None:
            self.deltas.append(price - last_price)
        else:
            self.deltas.append(None)

        return price

    def cache_sequences(self):
        for i in range(SEQ_LEN - 1, len(self.prices)):
            price = self.prices[i]
            start, end = i - 3, i + 1
            sequence = tuple(self.deltas[start:end])
            if sequence not in self.sequence_cache:
                self.sequence_cache[sequence] = price

def mix(result, secret):
    return result ^ secret

def prune(secret):
    return secret % 16777216

def iterate(seed, count):
    buyer = Buyer()

    secret = seed
    last_price = None
    for _ in range(count):
        last_price = buyer.append(secret, last_price)

        secret = prune(mix(secret * 64, secret))
        secret = prune(mix(secret // 32, secret))
        secret = prune(mix(secret * 2048, secret))

    return buyer

def get_total(sequence, buyers):
    total = 0
    for buyer in buyers:
        if sequence in buyer.sequence_cache:
            total += buyer.sequence_cache[sequence]

    return total

def find_optimal_sequence(buyers):
    for buyer in buyers:
        buyer.cache_sequences()
        # print(buyer.sequence_cache)

    seen = set()
    best_total = 0
    best_sequence = None
    for buyer in buyers:
        for sequence in buyer.sequence_cache:
            if sequence not in seen:
                seen.add(sequence)
                total = get_total(sequence, buyers)
                if total > best_total:
                    best_total = total
                    best_sequence = sequence
                    print(best_sequence, best_total)

    return best_sequence, best_total

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        buyer_seeds = [int(line.strip()) for line in file]
    # print(buyer_seeds)

    buyers = []
    for seed in buyer_seeds:
        buyers.append(iterate(seed, 2000))
        # print(steps)

    sequence, total = find_optimal_sequence(buyers)
    print(sequence)
    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-22")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
