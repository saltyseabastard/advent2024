import re

from aocd import data
from aocd import puzzle

def compute_phase_1():
    #print(data)
    example = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    abc_lines = [
        "ABC",
        "DEF",
        "GHI"
    ]

    simple_example = """..X...
.SAMX.
.A..A.
XMAS.S
.X...."""

    # Get length & width of data
    data_by_line = [list(line) for line in example.splitlines()]
    dataset_width = len(data_by_line[0]) #140
    dataset_height = len(data_by_line)   #140
    print(f"dataset_width = {dataset_width} dataset_height = {dataset_height}")

    # Create strings of line, column and diagonal
    # row strings
    row_strings = example.splitlines()

    # column strings
    column_strings = [""] * dataset_width

    for i in range(dataset_width):
        for line in data_by_line:
            column_strings[i] += line[i]

    print(f"column_strings = {len(column_strings)}")

    # diagonal strings
    south_west_strings = get_diagonals(abc_lines)
    print(f"south west strings: {south_west_strings}")
    south_east_strings = get_diagonals(reverse_columns(abc_lines))
    print(f"south east strings: {south_east_strings}")

    row_total_XMAS = get_match_from_string_list(r"XMAS", row_strings)
    print(f"row_total_XMAS = {row_total_XMAS}")
    row_total_SAMX = get_match_from_string_list(r"SAMX", row_strings)
    print(f"row_total_SAMX = {row_total_SAMX}")
    row_total = row_total_SAMX + row_total_XMAS
    col_total = get_match_from_string_list(r"XMAS", column_strings)
    col_total += get_match_from_string_list(r"SAMX", column_strings)
    sw_total = get_match_from_string_list(r"XMAS", south_west_strings)
    sw_total += get_match_from_string_list(r"SAMX", south_west_strings)
    se_total = get_match_from_string_list(r"XMAS", south_east_strings)
    se_total += get_match_from_string_list(r"SAMX", south_east_strings)

    print(f"row total: {row_total} col total: {col_total} nw total: {sw_total} se total: {se_total}")

    total_xmases = row_total + col_total + sw_total + se_total

    print(total_xmases)

def compute_phase_2():
    # Get length & width of data
    data_by_line = [list(line) for line in example.splitlines()]
    #data_by_line = [['S', 'Z', 'M'],
    #                ['A', 'A', 'A'],
    #                ['S', 'Z', 'M']]

    sams = 0
    for i in range(1, len(data_by_line) - 1):  # Adjust range as needed
        for j in range(1, len(data_by_line[i]) - 1):  # Adjust inner range as needed
            # print(f"data[{i}][{j}] = {data_by_line[i][j]}")
            if (
                    data_by_line[i][j] in {'A'}
                    and (data_by_line[i - 1][j - 1] is 'S' and data_by_line[i + 1][j + 1] is 'M'
                        or data_by_line[i - 1][j - 1] is 'M' and data_by_line[i + 1][j + 1] is 'S')
                    and (data_by_line[i + 1][j - 1] is 'S' and data_by_line[i - 1][j + 1] is 'M'
                        or data_by_line[i + 1][j - 1] is 'M' and data_by_line[i - 1][j + 1] is 'S')
            ):                sams += 1

    print(f"sams = {sams}")

def get_match_from_string_list(pattern, str_list):
    xmases = 0
    for r in str_list:
        matches = re.findall(pattern, r)

        if matches:  # Only append if matches is not empty
            xmases += len(matches)
    return xmases


def reverse_columns(lines):
    return [line[::-1] for line in lines]


def get_diagonals(lines):
    # Create an empty list for diagonals
    diagonals = []

    # Get the number of rows and columns
    num_rows = len(lines)
    num_cols = len(lines[0]) if num_rows > 0 else 0

    # Collect diagonals from top-left to bottom-right
    for diag in range(num_rows + num_cols - 1): # 5, the number of diagonals
        diagonal = []
        for row in range(num_rows): # 3
            col = diag - row  # Calculate column index
            if 0 <= col < num_cols:  # Ensure indices are in bounds
                diagonal.append(lines[row][col])
        diagonals.append("".join(diagonal))  # Join characters in each diagonal

    return diagonals
