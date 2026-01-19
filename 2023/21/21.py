import sys, os
import re
from queue import Queue
import numpy as np
from time import sleep

def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    n_rows = len(lines)
    n_cols = len(lines[0])
    grid = np.zeros((n_rows, n_cols))
    for y,row in enumerate(lines):
        for x,cell in enumerate(row):
            if cell == 'S':
                grid[y,x] = START
            elif cell == '#':
                grid[y,x] = ROCK
            elif cell == '.':
                grid[y,x] = PLOT

    return grid

PLOT = -1
START = -2
ROCK = 0
EXPLORED = 1

lookup = {
    PLOT: '.',
    ROCK: '#',
    START: 'S',
    EXPLORED: 'O'
}


def show_grid(grid, replace=False):
    for row in grid:
        line = [lookup.get(cell, str(int(cell))) for cell in row]
        if replace:
            print("".join(line), end='\r')
        else:
            print("".join(line))

def constrain(point, size):
    x = (point[0] + size[1]) % size[1]
    y = (point[1] + size[0]) % size[0]
    return (x,y)

def get_neighbours(curr, size, rocks, wraparound=False):
    n_rows = size[0]
    n_cols = size[1]
    
    (col, row) = curr
        
    nbs = [(col, row-1),(col+1, row),(col, row+1),(col-1, row)]

    if not wraparound:
        nbs = [
            nb for nb in nbs
            if nb[0] >= 0 and nb[0] < n_cols and nb[1] >= 0 and nb[1] < n_rows
        ]
    else:
        cnbs = [constrain(nb, size) for nb in nbs]

    not_rocks = [nb for nb,cnb in zip(nbs, cnbs) if cnb not in rocks]
    return not_rocks


def find_moves_per_cell(grid):
    neighbours_per_cell = []
    n_rows = grid.shape[0]
    n_cols = grid.shape[1]
    for y in range(n_rows):
        this_row_neighbours_per_cell = []
        for x in range(n_cols):
            nbs = []
            for nx,ny in [(x, y-1),(x+1, y),(x, y+1),(x-1, y)]:
                cnx,cny = constrain((nx,ny), grid.shape)
                if grid[cny][cnx] == PLOT:
                    nbs.append((nx-x,ny-y))
            this_row_neighbours_per_cell.append(np.array(nbs))
        neighbours_per_cell.append(this_row_neighbours_per_cell)
    return neighbours_per_cell


def find_reachable_points(grid, start, max_steps, wraparound=False):
    print(f"Finding reachability in {max_steps} steps from {start} (wraparound={wraparound})")

    reached_at = [set()]
    reached_at[0].add(tuple(start))

    seen = set()
    seen.add(tuple(start))

    n_rows, n_cols = tuple(grid.shape)
    ## Precompute the moves for each grid cell
    moves = find_moves_per_cell(grid)
    
    n_seen = np.zeros(max_steps+1,dtype=int)

    for steps in range(1, max_steps+1):
        # grid2 = grid.copy()
        newly_reached = set()
        
        for pt in reached_at[steps-1]:
            x,y = constrain(pt, grid.shape)
            nbs = np.add(np.array(moves[y][x]), np.array(pt))
            newly_reached = newly_reached.union([tuple(nb) for nb in nbs])
        
        ## Ignore any points we've already seen
        newly_reached = newly_reached.difference(seen)
        reached_at.append(newly_reached)
        ## Mark all these points as seen
        seen = seen.union(newly_reached)

        n_seen[steps] += len(newly_reached)
        if steps > 1:
            n_seen[steps] += n_seen[steps-2]
        print(f"Steps: {steps}, Seen: {n_seen[steps]}")

        
    return n_seen[steps]



def solve(fileaddr, num_steps, part=1):
    grid = read_file(fileaddr)
    wraparound = part == 2
    start = np.argwhere(grid == START)[0]
    n_reachable = 0
    # moves = find_moves_per_cell(grid)
    # print(moves)
    n_reachable = find_reachable_points(grid, start, num_steps, wraparound)
    return n_reachable






from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("filename", type=str)
    parser.add_argument("part", type=int, choices=[1,2])
    parser.add_argument("steps", type=int)
    args = parser.parse_args()

    filename = args.filename
    part = args.part
    num_steps = args.steps

    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + filename

    if os.path.exists(fileaddr):
        result = solve(fileaddr, num_steps, part)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
