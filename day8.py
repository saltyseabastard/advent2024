from aocd import data
from dataclasses import dataclass

from aocd_example_parser import simple

simple_example = """
..........
..........
..........
....a.....
..........
.....a....
..........
..........
..........
..........
"""
example = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

# Clean any \n's
stripped = example.strip()

# Parse into data arrays
data_by_line = [list(line) for line in data.splitlines()]

@dataclass(frozen=True)
class Antenna:
    row: int
    col: int

    def __hash__(self):
        # Hash based on tuple of attributes
        return hash((self.row, self.col))

    def __eq__(self, other):
        if not isinstance(other, Antenna):
            return NotImplemented
        # Equality based on attributes
        return self.row == other.row and self.col == other.col

antennas_by_symbol = {}

# Populate the various symbols and positions
for i in range(len(data_by_line)):
    for j in range(len(data_by_line[i])):
        if data_by_line[i][j] != ".":
            if data_by_line[i][j] not in antennas_by_symbol:
                antennas_by_symbol[data_by_line[i][j]] = [Antenna(i, j)]
            else:
                antennas_by_symbol[data_by_line[i][j]].append(Antenna(i, j))

def compute_phase_1():
    set_of_all_antinodes = set()
    for symbol in antennas_by_symbol:
        print("\n", symbol, antennas_by_symbol[symbol])
        antinodes = set()
        for i in range(len(antennas_by_symbol[symbol])):
            for j in range(i+1, len(antennas_by_symbol[symbol])):

                dist_by_row = antennas_by_symbol[symbol][i].row - antennas_by_symbol[symbol][j].row
                dist_by_col = antennas_by_symbol[symbol][i].col - antennas_by_symbol[symbol][j].col
                print(dist_by_row, dist_by_col)
                side1 = Antenna(antennas_by_symbol[symbol][i].row + dist_by_row, antennas_by_symbol[symbol][i].col + dist_by_col)
                side2 = Antenna(antennas_by_symbol[symbol][j].row - dist_by_row, antennas_by_symbol[symbol][j].col - dist_by_col)
                print("Antinodes pre-parse", side1, side2)
                if not (side1.row < 0 or side1.col < 0 or side1.row >= len(data_by_line) or side1.col >= len(data_by_line[0])):
                    antinodes.add(side1)
                if not (side2.row < 0 or side2.col < 0 or side2.row >= len(data_by_line) or side2.col >= len(data_by_line[0])):
                    antinodes.add(side2)

                print("Antinodes finally", side1, side2)

        for a in antinodes:
            set_of_all_antinodes.add(a)

    print(f"Total number of antinodes: {len(set_of_all_antinodes)}")
    # part 1 = 367

def compute_phase_2():
    set_of_all_antinodes = set()
    for symbol in antennas_by_symbol:
        print("\n", symbol, antennas_by_symbol[symbol])
        antinodes = set()
        for i in range(len(antennas_by_symbol[symbol])):
            for j in range(i + 1, len(antennas_by_symbol[symbol])):

                # add the og nodes because they are antinodes now
                antinodes.add(antennas_by_symbol[symbol][i])

                dist_by_row = antennas_by_symbol[symbol][i].row - antennas_by_symbol[symbol][j].row
                dist_by_col = antennas_by_symbol[symbol][i].col - antennas_by_symbol[symbol][j].col

                old_pos = Antenna(antennas_by_symbol[symbol][i].row,
                                antennas_by_symbol[symbol][i].col)
                while True:

                    side1 = Antenna(old_pos.row + dist_by_row, old_pos.col + dist_by_col)
                    if side1.row < 0 or side1.col < 0 or side1.row >= len(data_by_line) \
                        or side1.col >= len(data_by_line[0]):
                        break
                    else:
                        antinodes.add(side1)
                        old_pos = side1

                old_pos = Antenna(antennas_by_symbol[symbol][i].row,
                                  antennas_by_symbol[symbol][i].col)
                while True:

                    side2 = Antenna(old_pos.row - dist_by_row, old_pos.col - dist_by_col)

                    if side2.row < 0 or side2.col < 0 or side2.row >= len(data_by_line) \
                       or side2.col >= len(data_by_line[0]):
                        break
                    else:
                        antinodes.add(side2)
                        old_pos = side2


                print("Antinodes finally", side1, side2)

        for a in antinodes:
            set_of_all_antinodes.add(a)

    print(f"Total number of antinodes: {len(set_of_all_antinodes)}")
    # part 1 = 367

compute_phase_2()