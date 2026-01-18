
import numpy as np
from collections import defaultdict
# import regex as re

class Operation():
    pass

class CopyOp(Operation):
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.source_is_register = False
        try:
            self.source = int(self.source)
        except ValueError:
            self.source_is_register = True

class JumpNonzero(Operation):
    def __init__(self, source, n_steps):
        self.source = source
        self.n_steps = n_steps
        self.source_is_register = False
        try:
            self.source = int(self.source)
        except ValueError:
            self.source_is_register = True

    def __repr__(self):
        return f"Jnz({self.source}, steps={self.n_steps})"

class Inc(Operation):
    def __init__(self, register):
        self.register = register
    def __repr__(self):
        return f"Inc(r{self.register})"

class Dec(Operation):
    def __init__(self, register):
        self.register = register
    def __repr__(self):
        return f"Dec(r{self.register})"

## ===================================================

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    instructions = []
    for line in lines:
        splits = line.strip().split(" ")
        if splits[0] == 'cpy':
            source = splits[1]
            target = splits[2]
            instructions.append(CopyOp(source, target))
        elif splits[0] == 'inc':
            instructions.append(Inc(splits[1]))
        elif splits[0] == 'dec':
            instructions.append(Dec(splits[1]))
        elif splits[0] == 'jnz':
            instructions.append(JumpNonzero(splits[1], int(splits[2])))
    
    return instructions

"""
Instructions:

    cpy x y copies x (either an integer or the value of a register) into register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
"""

from typing import List

def run(instructions: List[Operation], registers=defaultdict(lambda: 0)):
    i = 0
    while i < len(instructions):
        instruction = instructions[i]
        assert isinstance(instruction, Operation)

        if isinstance(instruction, CopyOp):
            if instruction.source_is_register:
                val = registers[instruction.source]
            else:
                val = instruction.source
            registers[instruction.target] = val
        elif isinstance(instruction, Inc):
            registers[instruction.register] += 1
        elif isinstance(instruction, Dec):
            registers[instruction.register] -= 1
        elif isinstance(instruction, JumpNonzero):
            if instruction.source_is_register:
                val = registers[instruction.source]
            else:
                val = instruction.source
            
            if val != 0:
                i += instruction.n_steps
                continue

        i += 1
    
    return registers



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    instructions = load(fname)

    result = run(instructions)
    print("Part one:", result['a'])

    init_state = defaultdict(lambda:0)
    init_state['c'] = 1
    result = run(instructions, init_state)
    print("Part two:", result['a'])