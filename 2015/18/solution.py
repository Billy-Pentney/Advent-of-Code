import sys, os
import re

import numpy as np

def read_file(fileaddr):
    grid = []
    with open(fileaddr, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]
    return np.array(grid)



def get_neighbours(x,y,rows,cols):
    nbs = []
    for dx in range(-1,2):
        for dy in range(-1,2):
            if dx == 0 and dy == 0:
                continue
            nx,ny = x+dx,y+dy
            if nx >= 0 and nx < cols and ny >= 0 and ny < rows:
                nbs.append((nx,ny))
    return nbs


def show_grid(grid):
    for y in range(len(grid)):
        print("".join(grid[y]))


## Solve Part One
def part_one(fileaddr, n_iters, corners_on=False, show_steps=False):
    grid = read_file(fileaddr)

    rows = grid.shape[0]
    cols = grid.shape[1]

    grid[0][0] = '#'
    grid[0][cols-1] = '#'
    grid[rows-1][0] = '#'
    grid[rows-1][cols-1] = '#'

    show_grid(grid)
    print("Num iterations:", n_iters)

    for i in range(n_iters):
        new_grid = np.full(grid.shape, '.')

        for y in range(rows):
            for x in range(cols):
                if corners_on and x in [0, cols-1] and y in [0, rows-1]:
                    new_grid[y][x] = '#'
                    continue

                is_on = grid[y][x] == '#'
                on_nbs = sum([1 for nx,ny in get_neighbours(x,y,rows,cols) if grid[ny][nx] == '#'])
                if on_nbs == 3 or (is_on and on_nbs == 2):
                    new_grid[y][x] = '#'

        grid = new_grid
        if show_steps:
            print(f"After {i+1} steps...")
            show_grid(grid)
            print()
        

    print("After...")
    show_grid(grid)

    return np.sum(grid == '#', axis=(0,1))


## Solve Part Two
def part_two(fileaddr, n_iters):
    return part_one(fileaddr, n_iters, corners_on=True)










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]

    n_iters = int(args[1])
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    part_one_ans = part_one(fileaddr, n_iters)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    part_two_ans = part_two(fileaddr, n_iters)
    print(f"(Part 2) Solution: {part_two_ans}")
