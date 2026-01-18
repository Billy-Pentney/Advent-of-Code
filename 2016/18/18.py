
import numpy as np
import regex as re
# from collections import defaultdict

char_to_digit = {".":0,'^':1}

def load(fname):
    with open(fname, "r") as file:
        rows = [
            [char_to_digit[x] for x in row.strip("\n")] 
            for row in file.readlines()
        ]
    return rows

def convert_grid_to_ints(grid):
    """
    Converts a 2D grid of binary-string rows (0,1 characters only) into a list of integers.
    """
    return [
        int(re.sub(r"[\[\], \"]", "", str(row)), base=2) 
        for row in grid
    ]


def convert_grid_from_ints(grid, width):
    return [
        f"{num:b}".rjust(width, "0")
        for num in grid
    ]

## Enums
SAFE = 0
TRAP = 1

def expand_grid(grid, total_rows: int=40):
    """
    Simple solution; iteratively computes next row from the previous row, using the array form.
    """
    width = len(grid[0])

    while len(grid) < total_rows:
        last_row = grid[-1]
        curr_row = []
        
        for i in range(len(last_row)):
            is_trap = False
            left_is_trap = i >= 1 and last_row[i-1] == TRAP
            right_is_trap = i < width-1 and last_row[i+1] == TRAP
            ## This is a trap if exactly one of the sides is a trap
            is_trap = right_is_trap != left_is_trap
            this_tile = TRAP if is_trap else SAFE
            curr_row.append(this_tile)

        grid.append(curr_row)

    return grid

def expand_grid_and_count(grid, total_rows: int=4000):
    """
    Efficiently expands a large number of rows and returns the counts of the two types of tile.
    This implementation uses binary string and bitwise ops to speed-up the row computation.

    Returns:
    a dict with keys '0' and '1' indicating the counts of SAFE and TRAP tiles respectively.
    """
    counts = [0,0]
    counts[TRAP] = np.sum(grid, axis=(0,1))

    n_rows = len(grid)
    n_cols = len(grid[0])

    ## Convert the string based grid to their integer representation.
    ## We map '.' to 0 and '^' to 1.
    grid_ints = convert_grid_to_ints(grid)
    last_row_int = grid_ints[-1]

    for i in range(n_rows, total_rows):
        if i % 20000 == 0:
            print(f"Row {i}")

        ## We can use bitwise operations on the left-shifted and right-shifted strings e.g. 
        # if we have row "01101" (next row is "11100")
        # then we can do "011" XOR "101" (first-3-bits XOR last-3-bits) to find the "110", the middle 3 bits
        # then the first bit of the next row is the second bit of the previous row (1)
        # and the last bit of the next row is the second-to-last bit of the previous row (1).

        ## Worked Example:
            ## Row:               11001
            ## First 3 bits:       110
            ## Last 3 bits:        001
            ## A^B:                111      (middle bits of answer)

            ## (11001 & 01000) << 1 = 01000 << 1 = 10000
            ## Second bit:       1                          (first bit of answer)
            ## Second-last bit:  0                          (last bit of answer)

            ## Next row: B1 + (A^B << 1) + BL
            ##         = 10000 + 01110 + 00000 
            ##         = 11110

        ## Drop the last two bits
        last_row_1 = last_row_int >> 2
        ## Drop the first two bits
        last_row_2 = last_row_int & (pow(2, n_cols-2)-1)

        ## Take XOR to find the central part of the answer
        ## A bit is 1 if and only if the bit to its left and right are not the same!
        new_row_center = last_row_1 ^ last_row_2

        ## Second bit of the previous row
        new_row_first = last_row_int & pow(2, n_cols-2)
        ## Second-to-last bit of the previous row
        new_row_last = (last_row_int >> 1) % 2
        ## Concatenate together, sandwiching the XOR result
        last_row_int = (new_row_first << 1) + (new_row_center << 1) + new_row_last 
        ## Count the new Traps
        counts[TRAP] += sum([1 for b in f"{last_row_int:b}" if b=='1'])

    ## All tiles are either SAFE or TRAP, so find the desired count by subtraction
    counts[SAFE] = n_cols*total_rows - counts[TRAP]
    return counts


def count_safe_after_expansion(init_grid, height: int):
    counts = expand_grid_and_count(init_grid, height)
    return counts[SAFE]


from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    init_row = load(fname)

    num_safe = count_safe_after_expansion(init_row, 40)
    print("Part one:", num_safe)
    num_safe_large = count_safe_after_expansion(init_row, 400000)
    print("Part two:", num_safe_large)
