import re
from collections import deque
from itertools import groupby

from aocd import data
from dataclasses import dataclass
from functools import cache

simple_example = "0 1 10 99 999"
long_example = "125 17"
zero = "0"

dataset = list(map(int, data.split()))

def blink(stones, num_blinks):

    new_stones = stones.copy()
    for _ in range(num_blinks):
        new_stone_state = []
        for stone in new_stones:

            # Rule 1
            if stone == 0:
                new_stone_state.append(1)
            elif len(str(stone)) % 2 == 0:
                str_stone = str(stone)
                split_point= len(str_stone)//2
                new_stone_state.append(int(str_stone[:split_point]))
                new_stone_state.append(int(str_stone[split_point:]))
            else:
                new_stone_state.append(stone * 2024)

        new_stones = new_stone_state
        print(f"iteration {_} is {len(new_stones)}")

    return new_stones

@cache
def blink2(stone, steps):
    if steps == 0:
        return 1
    if stone == 0:
        return blink2(1, steps - 1)

    string = str(stone)
    length = len(string)
    if length % 2 == 0:
        return blink2(int(string[:length//2]), steps - 1) + blink2(int(string[length//2:]), steps - 1)

    return blink2(stone * 2024, steps - 1)

# print(f"Num stones = {len(blink(dataset, 25))}")
print(sum(blink2(stone, 75) for stone in dataset))

# test for learning, return fibonacci value at a position
@cache
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

print(f"Fib of 400 is: {fib(400)}")
