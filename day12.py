import re
from collections import deque
from itertools import groupby

from aocd import data
from dataclasses import dataclass

simple_example = """AAAA
BBCD
BBCC
EEEC"""

large_example = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

sides_large_example = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

e_example = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""

c_example = """CC
CB
CC"""

example_price_368 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

garden = data.strip().split("\n") # <-- Change here
puzzle_height = len(garden)
puzzle_width = len(garden[0])
print(f"garden {garden}")

# Use DFS to break down the garden into selected regions

#memo = {}
visited = set()

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

regions = []
def find_regions():

    for r in range(len(garden)):
        for c in range(len(garden[r])):
            if garden[r][c] not in visited:
                # this is a new region
                # perform a DFS here
                current_region = []
                dfs(current_region, garden[r][c], r, c)

                if len(current_region) > 0:
                    regions.append(current_region)

def dfs(current_region, letter, r, c):

    if (r, c) in visited:
        return

    if (letter, r, c) in current_region:
        return

    if garden[r][c] != letter:
        return

    current_region.append((letter, r, c))
    # add to visited
    visited.add((r,c))
    # for each dir in directions

    # for each neighbor
    for direction in directions:
        # if not marked
        nr = r + direction[0]
        nc = c + direction[1]

        if 0 <= nr < puzzle_height and 0 <= nc < puzzle_width:
            dfs(current_region, letter, nr, nc)

def find_perimeters_for_region(region):
    perimeter = 0
    coords = {(r, c) for (plant, r, c) in region}

    for (plant, r, c) in region:
        # Check neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            #if there is not a neighbor on this direction, add 1
            if (nr, nc) not in coords:
                    perimeter += 1

    #print(f"plant {plant} perimeter {perimeter}")
    return perimeter

def find_sides_for_region(region):
    edges = {}
    coords = {(r, c) for (plant, r, c) in region}

    for (plant, r, c) in region:
        # Check neighbors
        for index, dir in enumerate(directions):
            nr, nc = r + dir[0], c + dir[1]
            # if there is not a neighbor on this direction, add it's side to the set
            if (nr, nc) not in coords:
                match dir:
                    case (0, 1): # "right"
                        key = f"V{nc}R"
                        if key not in edges:
                            edges[key] = []
                        if (nr, nr+1) not in edges[key]:
                            edges[key].append((nr, nr+1))
                    case(0, -1):  # "left"
                        key = f"V{c}L"
                        if key not in edges:
                            edges[key] = []
                        if (nr, nr + 1) not in edges[key]:
                            edges[key].append((nr, nr + 1))
                    case (1, 0): # "down"
                        key = f"H{nr}D"
                        if key not in edges:
                            edges[key] = []
                        if (nc, nc-1) not in edges[key]:
                            edges[key].append((nc, nc + 1))
                    case (-1, 0): # "up"
                        key = f"H{r}U"
                        if key not in edges:
                            edges[key] = []
                        if (nc, nc - 1) not in edges[key]:
                            edges[key].append((nc, nc + 1))

    # conjoin edges into sides
    # split edges into cols and rows
    sides = 0
    for key, segments in edges.items():
        # Sort by start (the first number in start is the row or column)
        segments.sort(key=lambda x: x[0])
        merged = []
        for seg in segments:
            if not merged:
                merged.append(seg)
            else:
                last = merged[-1]
                # If seg starts right where last ends, merge them
                if seg[0] == last[1]:
                    merged[-1] = (last[0], seg[1])  # Extend the last segment
                else:
                    # Gap found, start a new segment
                    merged.append(seg)
        # Each merged segment = 1 side
        sides += len(merged)

    print(f"plant {plant} has {len(edges)} edges: {edges} and {sides} sides")
    return sides

find_regions()

total_perimeter = 0
total_price_pre_discount = 0
total_sides = 0
total_price_post_discount = 0

for region in regions:
    perimeter = find_perimeters_for_region(region)
    total_perimeter += perimeter
    total_price_pre_discount += perimeter * len(region)
    sides = find_sides_for_region(region)
    total_sides += sides
    total_price_post_discount += sides * len(region)


print(f"regions {regions}")
print(f"total_perimeter {total_perimeter}")
print(f"total_price_pre_discount {total_price_pre_discount}")
print(f"total_sides {total_sides}")
print(f"total_price_post_discount {total_price_post_discount}")

# Part 2
# 514604 too low
# 906824 too low