import re
from itertools import groupby

from aocd import data
from dataclasses import dataclass

simple_example = """0123
1234
8765
9876"""

split = simple_example.strip().split("\n")

print(split)

zeroes = []
# get all the zeroes
for i in range(len(split)):
    for j in range(len(split[i])):
        if split[i][j] == '0':
            zeroes.append((i, j))

print(zeroes)

# for each zero, track current number, proceed by 3x3 window

# count 9s

# bobs your uncle and fannie's your aunt