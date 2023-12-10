import sys, os
import re


"""
    | = vertical pipe connecting north and south.
    - = horizontal pipe connecting east and west.
    L = 90-degree bend connecting north and east.
    J = 90-degree bend connecting north and west.
    7 = 90-degree bend connecting south and west.
    F = 90-degree bend connecting south and east.
    . = no pipe in this tile.
    S = starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""

# MOVEMENT
UP = 'UP'
RIGHT = 'RIGHT'
DOWN = 'DOWN'
LEFT = 'LEFT'

VPIPE = '|'
HPIPE = '-'
LD = '7'
LU = 'J'
RD = 'F'
RU = 'L'


def get_enterable_neighbours(lines, start_pos, prev_pos=(-1,-1)):
    nbs = []
    (row, col) = start_pos
    (prow, pcol) = prev_pos

    # Move North from current
    if row > 0 and lines[row-1][col] in [VPIPE, LD, RD]:
        nbs.append((row-1,col,UP))
    # Move East from current
    if col < len(lines[row])-1 and lines[row][col+1] in [HPIPE, LU, LD]:
        nbs.append((row,col+1,RIGHT))
    # Move South from current
    if row < len(lines)-1 and lines[row+1][col] in [VPIPE, LD, RD]:
        nbs.append((row+1,col,DOWN))
    # Move West from current
    if col > 0 and lines[row][col-1] in [HPIPE, RU, RD]:
        nbs.append((row,col-1,LEFT))
    
    return [nb for nb in nbs if nb[0] != prow or nb[1] != pcol]



def get_next_cell_on_path(curr, curr_pos, prev_pos=(-1,-1)):
    (row, col) = curr_pos
    (prow, pcol) = prev_pos
    candidates = []

    if curr == VPIPE:   candidates = [(row-1,col,UP), (row+1,col,DOWN)]
    elif curr == HPIPE: candidates = [(row,col-1,LEFT), (row,col+1,RIGHT)]
    elif curr == RD:    candidates = [(row,col+1,RIGHT), (row+1,col,DOWN)]
    elif curr == LD:    candidates = [(row,col-1,LEFT), (row+1,col,DOWN)]
    elif curr == RU:    candidates = [(row,col+1,RIGHT), (row-1,col,UP)]
    elif curr == LU:    candidates = [(row,col-1,LEFT), (row-1,col,UP)]        

    return [nb for nb in candidates if nb[0] != prow or nb[1] != pcol]


def part_one(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    start_pos = None
    for r, line in enumerate(lines):
        for c, cell in enumerate(line):
            if (cell == 'S'):
                start_pos = (r,c)

    print("Start:", start_pos)

    nbs = get_enterable_neighbours(lines, start_pos)
    # Stores tuples of (cell, distance, previous cell) which should be considered by DFS
    to_check = []
    
    for nx, ny, move in nbs:
        to_check.append(((nx,ny), 1, start_pos))

    # For each cell in the loop, store its shortest distance to S
    dist_map = { start_pos: 0 }

    while len(to_check) > 0:
        (curr, d, prev) = to_check[0]
        to_check = to_check[1:]

        # New cell (not seen in loop)
        if curr not in dist_map.keys():
            dist_map[curr] = d
        else:
            break

        curr_sym = lines[curr[0]][curr[1]]

        next = get_next_cell_on_path(curr_sym, curr, prev)
        # print(next)
        for (x,y,move) in next:
            # print(move)
            to_check.append(((x,y), d+1, curr))

    return max(dist_map.values())



def part_two(fileaddr):
    ## Solve Part Two
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
