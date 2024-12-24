import re
from collections import deque
from itertools import groupby

from aocd import data
from dataclasses import dataclass

base_example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

dataset = base_example.strip().split("\n\n") # <-- Change here

@dataclass
class Machine:
    def __init__(self):
        self.A = None
        self.B = None
        self.Prize = None

# Function to parse individual entries
def parse_entry(entry):
    lines = entry.split('\n')
    machine = Machine()
    for line in lines:
        key, values = line.split(': ')
        x_val = int(values.split(', ')[0].split('+')[-1].split('=')[-1])
        y_val = int(values.split(', ')[1].split('+')[-1].split('=')[-1])

        if key == 'Button A':
            machine.A = (x_val, y_val)
        elif key == 'Button B':
            machine.B = (x_val, y_val)
        else:
            machine.Prize = (x_val, y_val)

    return machine

machines = [parse_entry(entry) for entry in dataset]

def get_button_presses(machine):
    # subtract button b(x, y) from prize until prize(x, y) are both divisible by a(x, y)
    subtracted_b = 0
    while machine.Prize[0] % machine.A[0] != 0 and machine.Prize[1] % machine.A[1] != 0:


    # count i, divide prize by a

    # multiply tokens