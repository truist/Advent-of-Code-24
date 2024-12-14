#!/usr/bin/env python3

"""
Advent of Code 2024-12
"""

import argparse
from dataclasses import dataclass

N = 0
E = 1
S = 2
W = 3

@dataclass
class Fence:
    segment: list

@dataclass
class PlantRecord:
    plant: str
    region: list
    row: int
    col: int
    fences: list

def neighbors(grid, r, c):
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        new_row = r + dr
        new_col = c + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
            yield new_row, new_col

def make_fences_record():
    return [Fence(None), Fence(None), Fence(None), Fence(None)]

def convert_plants_to_records(grid, r, c, plant, region):
    plant_record = PlantRecord(plant, region, r, c, make_fences_record())
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

def map_plant_fences(grid, plant_record):
    for new_row, new_col in neighbors(grid, plant_record.row, plant_record.col):
        if grid[new_row][new_col].plant == plant_record.plant:
            if new_row < plant_record.row:
                plant_record.fences[N] = None
            elif new_row > plant_record.row:
                plant_record.fences[S] = None
            elif new_col < plant_record.col:
                plant_record.fences[W] = None
            elif new_col > plant_record.col:
                plant_record.fences[E] = None

def get_neighbor(grid, r, c):
    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        return grid[r][c]

    return None

def merge_segments(grid, left, right, direction):
    new_segment = left + right
    # replace all the old segment records with the new one
    for segment_record in new_segment:
        grid[segment_record[0]][segment_record[1]].fences[direction].segment = new_segment

def make_segment_record(plant_record, direction):
    return [(plant_record.row, plant_record.col, direction)]

def add_fence_to_segment(has_segment, needs_segment, direction):
    has_segment.fences[direction].segment += make_segment_record(needs_segment, direction)
    needs_segment.fences[direction].segment = has_segment.fences[direction].segment

def group_fences(grid, middle, neighbor, direction):
    middle_segment = middle.fences[direction].segment
    neighbor_segment = neighbor.fences[direction].segment
    if middle_segment:
        if neighbor_segment:
            merge_segments(grid, middle_segment, neighbor_segment, direction)
        else:
            add_fence_to_segment(middle, neighbor, direction)
    elif neighbor_segment:
        add_fence_to_segment(neighbor, middle, direction)
    else:
        middle.fences[direction].segment = make_segment_record(middle, direction)
        add_fence_to_segment(middle, neighbor, direction)

def group_side(grid, middle, neighbor, direction):
    if neighbor:
        if middle.plant == neighbor.plant:
            if middle.fences[direction] and neighbor.fences[direction]:
                group_fences(grid, middle, neighbor, direction)

    if not middle.fences[direction].segment:
        middle.fences[direction].segment = make_segment_record(middle, direction)

def group_neighbors(grid, middle, side1, side2, direction):
    group_side(grid, middle, side1, direction)
    group_side(grid, middle, side2, direction)

def group_plant_fences(grid, plant_record):
    if plant_record.fences[N] or plant_record.fences[S]:
        west = get_neighbor(grid, plant_record.row, plant_record.col - 1)
        east = get_neighbor(grid, plant_record.row, plant_record.col + 1)
        if plant_record.fences[N]:
            group_neighbors(grid, plant_record, west, east, N)
        if plant_record.fences[S]:
            group_neighbors(grid, plant_record, west, east, S)

    if plant_record.fences[E] or plant_record.fences[W]:
        north = get_neighbor(grid, plant_record.row - 1, plant_record.col)
        south = get_neighbor(grid, plant_record.row + 1, plant_record.col)
        if plant_record.fences[E]:
            group_neighbors(grid, plant_record, north, south, E)
        if plant_record.fences[W]:
            group_neighbors(grid, plant_record, north, south, W)

def map_fences(grid, regions):
    for region in regions:
        for plant_record in region:
            map_plant_fences(grid, plant_record)

        for plant_record in region:
            group_plant_fences(grid, plant_record)

def get_distinct_segments(segments):
    distinct = set()
    for segment in segments:
        distinct.add(tuple(segment))

    return list(distinct)

def calc_region_price(region):
    region_segments = []
    for plant_record in region:
        for fence in plant_record.fences:
            if fence and fence.segment:
                region_segments += [fence.segment]

    return len(region) * len(get_distinct_segments(region_segments))

def main(inputfile):
    with open(inputfile, 'r', encoding='utf-8') as file:
        grid = [list(line.strip()) for line in file]

    regions = map_regions(grid)
    map_fences(grid, regions)

    total = 0
    for region in regions:
        total += calc_region_price(region)

    print(total)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2024-12")
    parser.add_argument("input", help="input data file")

    args = parser.parse_args()
    main(args.input)
