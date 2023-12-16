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


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]


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


def find_start_pos(lines):
    for r, line in enumerate(lines):
        for c, cell in enumerate(line):
            if (cell == 'S'):
                start_pos = (r,c)
    return start_pos


def run_dfs_on_path(lines, start_pos):
    nbs = get_enterable_neighbours(lines, start_pos)
    # Stores tuples of (cell, distance, previous cell) which should be considered by DFS
    frontier = [((nx,ny), 1, start_pos) for nx, ny, move in nbs]
    # For each cell in the loop, store its shortest distance to S
    dist_map = { start_pos: 0 }

    while len(frontier) > 0:
        # Remove the first element in the queue
        (curr, d, prev) = frontier[0]
        frontier = frontier[1:]

        # New cell (not seen in loop)
        if curr not in dist_map.keys():
            dist_map[curr] = d
        else:
            break

        curr_sym = lines[curr[0]][curr[1]]
        for (x,y,move) in get_next_cell_on_path(curr_sym, curr, prev):
            frontier.append(((x,y), d+1, curr))

    return dist_map


def part_one(fileaddr):
    lines = read_file(fileaddr)
    start_pos = find_start_pos(lines)
    print("Start:", start_pos)
    dist_map = run_dfs_on_path(lines, start_pos)
    return max(dist_map.values())


def identify_outside_loop(lines, loop):
    # Identify all cells which are not part of the loop
    non_loop_cells = [] 
    for r,row in enumerate(lines):
        for c,cell in enumerate(row):
            if (r,c) not in loop:
                non_loop_cells.append((r,c))

    to_check = []
    visited = {}

    # Get all non-loop cells on the outer edge of the grid
    for cell in non_loop_cells:
        if cell[0] == 0 or cell[0] == len(lines)-1 or cell[1] == 0 or cell[1] == len(lines[0])-1:
            to_check.append(cell)

    while len(to_check) > 0:
        curr = to_check[0]
        to_check = to_check[1:]
        visited[nb] = True

        for nb in get_all_neighbours(curr):
            if not visited[nb] and nb not in loop:
                to_check.append(nb)

    

    inner_cells = [cell for cell in non_loop_cells if not visited[cell]]
    return inner_cells


    
    




def part_two(fileaddr):
    lines = read_file(fileaddr)
    start_pos = find_start_pos(lines)
    print("Start:", start_pos)
    dist_map = run_dfs_on_path(lines, start_pos)

    path = list(dist_map.keys())
    print(path)

    elevation = []

    for r,row in enumerate(lines):
        row_elevation = []
        curr_elevation = 0
        for c,cell in enumerate(row):
            if (r,c) in dist_map:
                if curr_elevation == 0:
                    curr_elevation = 1
            elif curr_elevation == 1:
                curr_elevation = 0

            row_elevation.append(curr_elevation)
        elevation.append(row_elevation)

    for row in elevation:
        print(row)
                
    return 0









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
    
