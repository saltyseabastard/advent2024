import re
from collections import deque
from itertools import groupby

from aocd import data
from dataclasses import dataclass

simple_example = """0123
1234
8765
9876"""

fork_example = """0000000
0001000
0002000
6543456
7000007
8000008
9000009"""

four_example = """0090009
0001098
0002007
6543456
7650987
8760000
9870000"""

two_heads_example = """1000900
2000800
3000700
4567654
0008003
0009002
0000001"""

larger_example = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

three_branch_example = """9999909
9943219
9959929
9965439
9979949
1187651
1191111"""

thirteen_branch_example = """8890889
5551598
4442997
6543456
7658987
8761111
9871111"""

dataset = data.strip().split("\n") # <-- Change here
heights = [[int(c) for c in line] for line in dataset]

puzzle_height = len(heights)
puzzle_width = len(heights[0])

for height in heights:
    print(height)

digits = [set() for _ in range(10)]
trailheads = []

# get all the trailheads (zeroes)
for i in range(puzzle_height):
    for j in range(puzzle_width):
        if heights[i][j] == 0:
            trailheads.append((i,j))

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def reachable_nines_from(i, j):
    visited = set()
    q = deque()
    q.append((i, j, 0)) # we start from zero because that's always the trailhead start height
    visited.add((i, j, 0))
    reached_nines = set()

    while q: # we are popping off the left, so the queue shrinks as we go
        row, col, height = q.popleft()

        if height == 9:
            reached_nines.add((row, col))
            # don't break, there might be more paths

        if height < 9:
            next_height = height + 1
            for dir_col, dir_row in directions:
                next_row = row + dir_row
                next_col = col + dir_col
                if 0 <= next_row < puzzle_height and 0 <= next_col < puzzle_width:
                    if heights[next_row][next_col] == next_height and (next_row, next_col) not in visited:
                        visited.add((next_row, next_col))
                        q.append((next_row, next_col, next_height))

    return reached_nines

memo = {}
def count_paths(r, c):

    if (r, c) in memo:
        return memo[(r, c)]

    current_height = heights[r][c]

    # base case, start unwinding from here
    if current_height == 9:
        memo[(r, c)] = 1
        return 1

    next_height = current_height + 1
    total_trails = 0

    for dir_col, dir_row in directions:
        next_row = r + dir_row
        next_col = c + dir_col
        if 0 <= next_row < puzzle_height and 0 <= next_col < puzzle_width:
            if heights[next_row][next_col] == next_height:
                trails_from_neighbor = count_paths(next_row, next_col)
                total_trails += trails_from_neighbor

    memo[(r, c)] = total_trails
    return total_trails

all_trails_score = 0
distinct_branches_score = 0

for (r, c) in trailheads:
    nines = reachable_nines_from(r, c)
    all_trails_score += len(nines)

for (r, c) in trailheads:
    rating = count_paths(r, c)
    distinct_branches_score += rating

# count 9s
print (f"High points accessible by path: {all_trails_score}")
print (f"Distinct trails: {distinct_branches_score}")

# bobs your uncle and fannie's your aunt
# part 1
# 276 too low
# Answer = 744

