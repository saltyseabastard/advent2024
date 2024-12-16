import re
from itertools import groupby

from aocd import data
from dataclasses import dataclass

simple_example = "12345"
# expanded
# 0x1 1x3   2x5
# 0..111....22222

example = "2333133121414131402"

input_data = list(data) # <---------- Change only me!
print (input_data)
# Convert to integers
int_array = [int(x) for x in input_data]

def expand_with_file_id(list_to_expand):
    expanded_str = []

    current_file_id = 0
    # iterate through and get the even numbers
    for i in range(len(list_to_expand)):
        if i % 2 == 0:
            expanded = [f"{current_file_id}"] * list_to_expand[i]
            expanded_str += expanded
            current_file_id += 1
        else:
            expanded_str += ["."] * list_to_expand[i]

    return expanded_str

def move_file_blocks(int_list):
    lowest_pick_from_right = len(int_list)
    for i in range(len(int_list)):
        if i >= lowest_pick_from_right - 1:
            break
        if int_list[i] == ".":
            for j in range(len(int_list) - 1, len(int_list) - i -2, -1):
                if int_list[j] != ".":
                    lowest_pick_from_right = j
                    int_list[i] = int_list[j]
                    int_list[j] = "."
                    break


def move_file_blocks_by_group(grouped_nested_list):
    #lowest_pick_from_right = len(grouped_nested_list)
    source = [block[:] for block in grouped_nested_list]
    numbers_tested = []
    i = 0
    while i < len(source):
        # if we are in a gap
        if source[i][0] == ".":
            # start from the end, find the first one that fits in this gap
                for j in range(len(source) - 1, i, -1):
                    if source[j][0] == ".":
                        continue
                    if source[j][0] not in numbers_tested:
                        numbers_tested.append(source[j][0])
                    else:
                        continue
                    if len(source[i]) >= len(source[j]):

                         # get just the first number in the group
                        len_diff = len(source[i]) - len(source[j])
                        sideA = source[j]
                        sideB = ['.'] * len(source[j])
                        new_gap = (['.'] * len_diff)
                        source[i] = sideA

                        if source[j-1][0] == ".":
                            source[j-1].extend(sideB)
                        else:
                            source[j] = sideB

                        if len(new_gap) > 0:
                            source.insert(i + 1, new_gap) # we have to do this after because the index has changed
                            i+=1 # we're still iterating, so make sure we skip the new gap
                        break

        i+=1

    return source


def move_files_to_leftmost_spaces(line_of_groups):
    # Flatten to a single list for easier manipulation
    line = [block for group in line_of_groups for block in group]

    # Identify files: anything that’s not '.' is a file block
    # We'll store files as: {file_id: [(start_index, length_of_file), ...]}
    # Though each file should be contiguous, we’ll confirm by scanning.
    files = {}
    visited = [False] * len(line)

    for i, ch in enumerate(line):
        if ch != '.' and not visited[i]:
            # Found the start of a file sequence
            file_id = ch
            start = i
            # Move forward until we hit a non-matching char or end
            j = i
            while j < len(line) and line[j] == file_id:
                visited[j] = True
                j += 1
            length = j - start
            files[file_id] = (start, length)

    # Sort files by descending file ID (numerical)
    # File IDs are strings of digits, so convert to int
    sorted_files = sorted(files.items(), key=lambda x: int(x[0]), reverse=True)

    for file_id, (start, length) in sorted_files:
        # Current file occupies line[start : start+length]

        # We need to find a gap to the left that fits 'length' dots
        # Let's scan from left to right, stopping before we reach the file start
        candidate_start = None
        candidate_length = 0
        best_start = None

        for idx in range(start):
            if line[idx] == '.':
                if candidate_start is None:
                    candidate_start = idx
                    candidate_length = 1
                else:
                    candidate_length += 1
                # Check if this gap fits our file
                if candidate_length == length:
                    # We found a perfect gap
                    best_start = candidate_start
                    break
            else:
                # Reset gap search if we hit a non-dot
                candidate_start = None
                candidate_length = 0

        if best_start is not None:
            # Move the file to that gap
            # 1) Clear original location
            for i in range(start, start + length):
                line[i] = '.'
            # 2) Place file into the new gap
            for i in range(best_start, best_start + length):
                line[i] = file_id
            # Update the file's recorded position (if you need it)
            files[file_id] = (best_start, length)

    # If you need to re-group the line_of_groups, you can,
    # but if just returning the flattened line is okay:
    return line

def split_to_grouped_array(int_list):
    lol = []
    last_char = int_list[0]
    for i in range(len(int_list)):
        if int_list[i] == last_char:
            if lol[len(lol) - 1] == int_list[i]:
                lol[len(lol) - 1].append(int_list[i])
            else:
                lol.append([last_char])

    return lol

def get_checksum(int_list):
    checksum = 0
    for i in range(len(int_list)):
        cs = int_list[i] * i
        #print(f"{int_list[i]} * {i} = {cs} == {cs+checksum}")
        checksum += cs
    return checksum

result = expand_with_file_id(int_array)
print(f"result {result}")

# combine into string
joined_string = "".join(result)

grouped_array = [list(group) for _, group in groupby(joined_string)]

print(f"grouped_array {grouped_array}")

gpt_answer = move_files_to_leftmost_spaces(grouped_array)

print(f"gpt_answer {gpt_answer}")


#move_file_blocks(result) # part 1
#print(f"move_file_blocks {int_array}")

# for i in range(len(grouped_array)):
#     grouped_array = move_file_blocks_by_group(grouped_array)
#     #print(f"move_file_blocks {grouped_array}")
#
# print(f"final move_file_blocks {grouped_array}")
#
# parse dots
#cleaned_array = [element for element in result if element != '.']
#print(f"clean {cleaned_array}")

# remove dots from grouped array
#filtered_array = [element for element in grouped_array if '.' not in element]
#print(f"filtered {filtered_array}")

# Replace lists with '.' with [0]
for i in range(len(grouped_array)):
    for j in range(len(grouped_array[i])):
        if grouped_array[i][j] == '.':
            grouped_array[i][j] = '0'

#cleaned_array = [[0] if '.' in sublist else list(map(int, sublist)) for sublist in grouped_array]
#print(f"clean {cleaned_array}")

# convert int
for i in range(len(gpt_answer)):
    if gpt_answer[i] == '.':
        gpt_answer[i] = 0
    else:
        gpt_answer[i] = int(gpt_answer[i])

print(f"gpt_answer post int {gpt_answer}")
#int_array = [[int(x) for x in sublist] for sublist in gpt_answer]

#break down internal arrays
# flattened_array = [item for sublist in int_array for item in sublist]
# print(f"flattened {flattened_array}")
# convert int
# int_array = [int(x) for x in filtered_array]
# print (f"int_array {int_array}")

og_test = "0099811188827773336446555566" # checksum 1928 - correct
test = "0099211177744333555566668888"
new_test = "009921117770440333000055550666600000888800" #<-- this is the one that works

#test_arr = list(new_test)
#int_array = [int(x) for x in test_arr]
checksum = get_checksum(gpt_answer)

print(checksum)

# 956924444 too low
# Part 1: 6337921897505
# 116340675768 too low