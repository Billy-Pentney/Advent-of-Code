
import numpy as np
import regex as re
from typing import List
from abc import ABC

class Transformation(ABC):
    """
    An abstract class for an operation that can be applied to a 2D grid.
    """
    def apply_to(self, grid):
        pass

class Rect(Transformation):
    """Draws a rectangle of the given dimensions, starting from the top-left (0,0) of the grid."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def __repr__(self):
        return f"Rect(w={self.width}, h={self.height})"
    
    def apply_to(self, grid):
        grid[:self.height, :self.width] = '#'
        return grid


class RotateCol(Transformation):
    """ Shifts the contents of the specified column by an amount, with wraparound back to the start. """
    def __init__(self, col, amt):
        self.col = col
        self.amt = amt
    def __repr__(self):
        return f"Rotate-Col(x={self.col}, amt={self.amt})"
    def apply_to(self, grid):
        grid[:,self.col] = np.roll(grid[:,self.col], self.amt)
        return grid

class RotateRow(Transformation):
    """ Shifts the contents of the specified row by an amount, with wraparound back to the start. """
    def __init__(self, row, amt):
        self.row = row
        self.amt = amt
    def __repr__(self):
        return f"Rotate-Row(y={self.row}, amt={self.amt})"
    def apply_to(self, grid):
        grid[self.row, :] = np.roll(grid[self.row, :], self.amt)
        return grid



## Regex pattern to parse a rotation instruction
## * Group 1 - indicates "row" or "column"
## * Group 2 - the index for the row/column
## * Group 3 - the amount of cells to shift by
rotate_pattern = r"rotate (row|column) (?:y|x)=(\d+) by (\d+)"

def load(fname):
    with open(fname, "r") as file:
        instructions = [row.strip("\n") for row in file.readlines()]

    final_instructions = []
    for instruction in instructions:
        if instruction.startswith("rect"):
            splits = instruction.split(" ")
            dims = [int(dim) for dim in splits[1].split("x")]
            final_instructions.append(Rect(dims[0], dims[1]))
            continue
        
        match = re.match(rotate_pattern, instruction)
        if match:
            type_rotation = match.group(1)
            index = int(match.group(2))
            amt = int(match.group(3))
            if type_rotation == 'column':
                final_instructions.append(RotateCol(index, amt))
            elif type_rotation == 'row':
                final_instructions.append(RotateRow(index, amt))
        else:
            print(f"Did not match instruction '{instruction}'")

    return final_instructions


def count_visible(grid, target='#'):
    return np.sum(grid == target)

def show(grid):
    for y in range(grid.shape[0]):
        print("".join(grid[y]))
    print()


def perform_instructions(instructions: List[Transformation], init_shape=(6,50), verbose=False):
    grid = np.full(init_shape, '.')
    for instruction in instructions:
        if verbose:
            print(instruction)
        grid = instruction.apply_to(grid)
        if verbose:
            show(grid)
    return grid


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    instructions = load(fname)
    init_shape = (3,10) if fname == 'example.txt' else (6,50)
    verbose = fname == 'example.txt' 
    
    grid = perform_instructions(instructions, init_shape, verbose)
    part_one = count_visible(grid)
    print("Part one:",part_one)

    print("Part two:")
    ## Display the final grid and read the output manually
    show(grid)