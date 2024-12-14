#!/usr/bin/env python3

"""
Advent of Code 2024-12
"""

import argparse
from dataclasses import dataclass

@dataclass
class PlantRecord:
    plant: str
    region: list
    row: int
    col: int

def neighbors(grid, r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row = r + dr
        new_col = c + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            yield new_row, new_col


def convert_plants_to_records(grid, r, c, plant, region):
    plant_record = PlantRecord(plant, region, r, c)
    grid[r][c] = plant_record
    region += [plant_record]

    for new_row, new_col in neighbors(grid, r, c):
        # print(f"{new_row},{new_col}={grid[new_row][new_col]}, plant={plant}")
        if grid[new_row][new_col] == plant:
            # print("found match! converting...")
            convert_plants_to_records(grid, new_row, new_col, plant, region)

def map_regions(grid):
    regions = []
    for r in range(len(grid)): # pylint: disable=consider-using-enumerate
        for c in range(len(grid[0])):
            if isinstance(grid[r][c], str):
                # print(f"found new plant at {r},{c}: {grid[r][c]}")
                region = []
                regions.append(region)
                convert_plants_to_records(grid, r, c, grid[r][c], region)

    return regions

def calc_plant_fence(grid, plant_record):
    fence = 4
    for new_row, new_col in neighbors(grid, plant_record.row, plant_record.col):
        if grid[new_row][new_col].plant == plant_record.plant:
            fence -= 1

    return fence

def calc_region_price(grid, region):
    total_fence = 0
    for plant_record in region:
        total_fence += calc_plant_fence(grid, plant_record)

    # print(f"region with {region[0].plant} has area {len(region)} and fence {total_fence}")
    return total_fence * len(region)

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    regions = map_regions(grid)
    # print(grid)
    # print(regions)

    total = 0
    for region in regions:
        total += calc_region_price(grid, region)

    print(total)

    # iterate the map, collecting region records
        # map from cell to region
        # map from region to cells
    # region area is easy
    # walk each region to calculate perimeter
    # calculate total price

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-12")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
