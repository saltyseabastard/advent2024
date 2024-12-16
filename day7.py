import re
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from aocd import data
import sys
import copy
from itertools import product

example = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

# Initialize two arrays
keys = []
values = []

# Parse the data
for line in data.strip().splitlines():
    key, value = line.split(": ")
    keys.append(int(key))
    values.append(list(map(int, value.split())))

# Print the results
print("Keys:", keys)
print("Values:", values)

total = 0

def compute_phase_1():

    global total
    for i in range(len(keys)):

        numbers = values[i]
        operators = list(product("+*", repeat=(len(numbers) - 1)))

        print(f"\n---- Evaluating {keys[i]} ----")
        # Apply each combination
        for op in operators:

            # start with the first number
            result = numbers[0]

            # get the num nums
            for num in range(1, len(numbers)):
                if op[num-1] == "*":
                    result *= numbers[num]
                elif op[num-1] == "+":
                    result += numbers[num]

            if result == keys[i]:
                print (f"DING!! {keys[i]} -> {result}")
                total += result
                break

    print (f"\nTotal: {total}")

def compute_phase_2():

    global total

    for i in range(len(keys)):

        numbers = values[i]
        operators = list(product("+*|", repeat=(len(numbers) - 1)))
        print(operators)

        print(f"\n---- Evaluating {keys[i]} ----")
        # Apply each combination
        for op in operators:

            # start with the first number
            result = numbers[0]

            # get the num nums
            for num in range(1, len(numbers)):
                if op[num-1] == "*":
                    result *= numbers[num]
                elif op[num-1] == "+":
                    result += numbers[num]
                elif op[num-1] == "|":
                    concat = str(result) + str(numbers[num])
                    result = int(concat)

            if result == keys[i]:
                print (f"DING!! {keys[i]} -> {result}")
                total += result
                break

    print (f"\nTotal: {total}")

compute_phase_2()
