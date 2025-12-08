
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(grid)


def count_splits(grid, count_timelines=False):
    start_pos = (0,0)
    n_rows = grid.shape[0]
    n_cols = grid.shape[1]
    for x in range(n_cols):
        for y in range(n_rows):
            if grid[y,x] == 'S':
                start_pos = (x,y)
                break

    n_splits = 0

    start_x, start_y = start_pos
    beam_prev = [start_x]
    beam_new = []

    ## Count the number of particles that reach each cell of the grid.
    ## This is equivalent to the number of timelines that reach that cell.
    particles_reaching = np.zeros(grid.shape, dtype=np.int64)
    particles_reaching[start_y, start_x] = 1

    for y in range(start_y+1, n_rows):
        # print(beam_prev)
        for x in beam_prev:
            if grid[y,x] == '^' and y < n_rows-1:
                n_splits += 1
                ## Split one left and one right
                if x > 0:
                    particles_reaching[y,x-1] += particles_reaching[y-1,x]
                    grid[y,x-1] = '|'
                    beam_new.append(x-1)
                if x < n_cols-1:
                    particles_reaching[y,x+1] += particles_reaching[y-1,x]
                    grid[y,x+1] = '|'
                    beam_new.append(x+1)
            else:
                ## Move down
                particles_reaching[y,x] += particles_reaching[y-1,x]
                grid[y,x] = '|'
                beam_new.append(x)

        ## Remove duplicates and iterate
        beam_prev = list(set(beam_new))
        beam_new = []


    if count_timelines:
        ## Count the total particles reaching the last row
        return np.sum(particles_reaching[-1,:], dtype=np.int64)
    else:
        return n_splits




from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)
    # print(grid)

    part_one = count_splits(grid)
    print("Part 1:", part_one)

    part_two = count_splits(grid, count_timelines=True)
    print("Part 2:", part_two)
