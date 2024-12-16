import re
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from aocd import data
import sys
import copy

example = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

# Clean any \n's
stripped = example.strip()

# Parse into data arrays
data_by_line = [list(line) for line in data.splitlines()]

guard_pos = (0,0)
guard_dir = "^"

def compute_phase_1():
    global guard_pos, guard_dir, data_by_line
    guard_pos, guard_dir = get_guard_pos_and_dir()
    print(f"Guard start pos: {guard_pos}, dir {guard_dir}")

    # set current pos to X since he will move
    data_by_line[guard_pos[0]][guard_pos[1]] = "X"

    # get steps to next obstruction
    total_steps_taken = 0

    while True:
        steps_taken = 0
        # set current pos to X since he will move
        data_by_line[guard_pos[0]][guard_pos[1]] = "X"

        if guard_dir == "^":
            for i in range(guard_pos[0] - 1, -1, -1):
                if data_by_line[i][guard_pos[1]] != "#":
                    data_by_line[i][guard_pos[1]] = "X"
                    print(f"step {i} {guard_pos[1]}")
                    steps_taken += 1
                    total_steps_taken += 1
                else:
                    break

            # move guard
            guard_pos = (guard_pos[0] - steps_taken, guard_pos[1])

            if guard_pos[0] == 0:
                break

        elif guard_dir == "v":
            for i in range(guard_pos[0] + 1, len(data_by_line), 1):
                if data_by_line[i][guard_pos[1]] != "#":
                    data_by_line[i][guard_pos[1]] = "X"
                    print(f"step {i} {guard_pos[1]}")
                    steps_taken += 1
                    total_steps_taken += 1
                else:
                    break

            # move guard
            guard_pos = (guard_pos[0] + steps_taken, guard_pos[1])

            if guard_pos[0] == len(data_by_line) - 1:
                break

        elif guard_dir == ">":
            for i in range(guard_pos[1] + 1, len(data_by_line[0]), 1):
                if data_by_line[guard_pos[0]][i] != "#":
                    data_by_line[guard_pos[0]][i] = "X"
                    print(f"step {guard_pos[0]} {i}")
                    steps_taken += 1
                    total_steps_taken += 1
                else:
                    break

            # move guard
            guard_pos = (guard_pos[0], guard_pos[1] + steps_taken)

            if guard_pos[1] == len(data_by_line[0]) - 1:
                break

        elif guard_dir == "<":
            for i in range(guard_pos[1] - 1, -1, -1):
                if data_by_line[guard_pos[0]][i] != "#":
                    data_by_line[guard_pos[0]][i] = "X"
                    print(f"step {guard_pos[0]} {i}")
                    steps_taken += 1
                    total_steps_taken += 1
                else:
                    break

            # move guard
            guard_pos = (guard_pos[0], guard_pos[1] - steps_taken)

            if guard_pos[1] == 0:
                break

        turn_90_right()  # sets new guard dir at position
        print(f"Steps taken: {steps_taken}")
        print(f"New guard pos: {guard_pos}, dir {guard_dir}")

    print(f"Steps taken: {steps_taken}")
    print("Guard has left the building!")

    for _ in range(len(data_by_line)):
        print(data_by_line[_])

    total_xs = sum(row.count("X") for row in data_by_line)
    print(f"Total Xs left on the map: {total_xs}")

def turn_90_right():
    global guard_dir
    if guard_dir == "^":
        guard_dir = ">"
    elif guard_dir == ">":
        guard_dir = "v"
    elif guard_dir == "v":
        guard_dir = "<"
    elif guard_dir == "<":
        guard_dir = "^"

    data_by_line[guard_pos[0]][guard_pos[1]] = guard_dir

def get_guard_pos_and_dir():
    global guard_pos, guard_dir
    for i in range(len(data_by_line)):  # Iterate over indices of data_by_line
        for j in range(len(data_by_line[i])):  # Iterate over indices within each line
            if data_by_line[i][j] == "^" or data_by_line[i][j] == ">" or data_by_line[i][j] == "<" or data_by_line[i][j] == "v":
                guard_pos = (i, j)
                guard_dir = data_by_line[i][j]
    return guard_pos, guard_dir

@dataclass(frozen=True)
class State:
    row: int
    col: int
    dir: ""

def compute_phase_2():
    global guard_pos, guard_dir, data_by_line
    guard_pos, guard_dir = get_guard_pos_and_dir()
    print(f"Guard start pos: {guard_pos}, dir {guard_dir}")

    infinite_loops = 0

    # cache dbl
    og_data_by_line = copy.deepcopy(data_by_line)

    for r in range(len(data_by_line)):
        for c in range(len(data_by_line[r])):

            steps_taken = 0

            #reset sim
            data_by_line = copy.deepcopy(og_data_by_line)
            guard_pos, guard_dir = get_guard_pos_and_dir()
            visited_states = set()

            #try one
            if data_by_line[r][c] == "#":
                continue

            #start the bruteforce
            data_by_line[r][c] = "#"
            print(f"***** Bruteforcing {r} {c}")
            for _ in range(len(data_by_line)):
                print(data_by_line[_])
            infinite_loop = False

            while True:
                steps_taken = 0
                # set current pos to NESW since he will move
                data_by_line[guard_pos[0]][guard_pos[1]] = "X"
                visited_states.add(State(guard_pos[0], guard_pos[1], guard_dir))

                if guard_dir == "^":
                    for i in range(guard_pos[0] - 1, -1, -1):
                        if data_by_line[i][guard_pos[1]] != "#":
                            new_state = State(i, guard_pos[1], guard_dir)
                            if new_state in visited_states:
                                infinite_loop = True
                                break
                            visited_states.add(new_state)
                            data_by_line[i][guard_pos[1]] = "X"
                            steps_taken += 1
                        else:
                            break

                    # move guard
                    guard_pos = (guard_pos[0] - steps_taken, guard_pos[1])
                    if guard_pos[0] == 0:
                        break

                elif guard_dir == "v":
                    for i in range(guard_pos[0] + 1, len(data_by_line), 1):
                        if data_by_line[i][guard_pos[1]] != "#":
                            new_state = State(i, guard_pos[1], guard_dir)
                            if new_state in visited_states:
                                infinite_loop = True
                                break
                            visited_states.add(new_state)
                            data_by_line[i][guard_pos[1]] = "X"
                            steps_taken += 1
                        else:
                            break

                    # move guard
                    guard_pos = (guard_pos[0] + steps_taken, guard_pos[1])

                    if guard_pos[0] == len(data_by_line) - 1:
                        break

                elif guard_dir == ">":
                    for i in range(guard_pos[1] + 1, len(data_by_line[0]), 1):
                        if data_by_line[guard_pos[0]][i] != "#":
                            new_state = State(guard_pos[0], i, guard_dir)
                            if new_state in visited_states:
                                infinite_loop = True
                                break
                            visited_states.add(new_state)
                            data_by_line[guard_pos[0]][i] = "X"
                            steps_taken += 1
                        else:
                            break

                    # move guard
                    guard_pos = (guard_pos[0], guard_pos[1] + steps_taken)

                    if guard_pos[1] == len(data_by_line[0]) - 1:
                        break

                elif guard_dir == "<":
                    for i in range(guard_pos[1] - 1, -1, -1):
                        if data_by_line[guard_pos[0]][i] != "#":
                            new_state = State(guard_pos[0], i, guard_dir)
                            if new_state in visited_states:
                                infinite_loop = True
                                break
                            visited_states.add(new_state)
                            data_by_line[guard_pos[0]][i] = "X"
                            steps_taken += 1
                        else:
                            break

                    # move guard
                    guard_pos = (guard_pos[0], guard_pos[1] - steps_taken)

                    if guard_pos[1] == 0:
                        break

                if infinite_loop:
                    infinite_loops += 1
                    print(f"Infinite loops: {infinite_loops}")
                    break

                turn_90_right()  # sets new guard dir at position

    print(f"Total infinite loops: {infinite_loops}")

compute_phase_2()
#16081 too high