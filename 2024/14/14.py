

from sys import argv
from os.path import exists
from os import makedirs
from time import sleep


import regex as re
import numpy as np



## Matches a position and velocity e.g. "p=100,201 v=98,-1"
robot_re = re.compile("p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


def load(fname):
    with open(fname, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    robots = []
    for line in lines:
        match = robot_re.match(line)
        if match:
            x = int(match[1])
            y = int(match[2])
            vx = int(match[3])
            vy = int(match[4])
            robots.append((x,y,vx,vy))

    return robots


def convert_to_grid(robots, size):
    """ Constructs a new 2D integer array describing the number of robots at each location in the grid. """
    grid = np.full(size, 0)
    for robot in robots:
        x,y,_,_  = robot
        # print(f"Robot {robot} at ({x},{y})")
        grid[x][y] = grid[x][y]+1
    
    # Flip from column-major to row-major
    return grid.T




def part_one(robots, size, iters=100):

    cols,rows = size

    for i in range(iters):
        for r, robot in enumerate(robots):
            (x,y,vx,vy) = robot
            x_ = (x+vx+cols)%cols
            y_ = (y+vy+rows)%rows
            robots[r] = (x_,y_,vx,vy)

   

    grid = convert_to_grid(robots, size)

    ## Now, count the number of robots in each quadrant
    hc = cols//2
    hr = rows//2

    quadrants = [
        (0, hr, 0, hc),         ## Upper-left
        (rows-hr, rows, 0, hc), ## Lower-left
        (0, hr, cols-hc, cols), ## Upper-right
        (rows-hr, rows, cols-hc, cols)  ## Lower-right
    ]
    quad_counts = [0,0,0,0]

    for i,quad in enumerate(quadrants):
        y1,y2,x1,x2 = quad
        quad_counts[i] = np.sum(grid[y1:y2,x1:x2])

    return np.product(quad_counts)



def write_grid_to(grid, fname):
    """ Saves a 2D array to the given filepath. """
    with open(fname, "w") as file:
        str_grid = ["".join(list(map(str, row)))+"\n" for row in grid]
        str_grid = [row.replace('0', '.') for row in str_grid]
        file.writelines(str_grid)


def neighbours(x, y, rows, cols):
    """ Get the adjacent neighbours of the given cell that are within the given bounds."""
    nbs = []
    if x >= 0:
        nbs.append((x-1,y))
    if x < cols:
        nbs.append((x+1,y))
    if y >= 0:
        nbs.append((x,y-1))
    if y < rows:
        nbs.append((x,y+1))
    return nbs




def has_k_consecutive_ones(arr, k):
    """ Check if the array contains a contiguous subarray with at least k '1's. """

    kernel = np.ones(k, dtype=int)
    convolved = np.apply_along_axis(
        lambda row: np.convolve(row, kernel, mode='valid'), axis=1, arr=arr
    )
    # Check if any value in the convolved array equals k
    return np.any(convolved == k)


def check_for_tree(robots, size, start, end, delay_ms=1000, save_to=None):
    """
        Solves part 2 by running the simulation for the given iteration range and checking if a sufficient consecutive number of 1s is seen in any row of the grid.

        Params
        ---
        robots: list
            list of robots, 4-tuples (x,y,vx,vy) where x,y is the coordinates and vx,vy is the velocity vector
        size: 2-tuple 
            size of the grid, row-first
        start: int
            Number of iterations to run before checking for the tree
        end: int
            Maximum number of iterations before stopping
        delay_ms: int
            Number of milliseconds between each iteration.
        save_to: str or None
            Name of the directory to save the viable grids.

    """

    if start > 0:
        ## Skip the first (start) seconds
        for r,robot in enumerate(robots):
            x,y,vx,vy = robot
            nx = (start * (x+vx)) % size[0]
            ny = (start * (y+vy)) % size[1]
            robots[r] = (nx,ny,vx,vy)

    # Delay in seconds
    delay = delay_ms / 1000

    # Run the remaining iterations
    for i in range(start, end):
        if (i+1) % 1000 == 0:
            print(f"ITERATION {i+1}")

        for r,robot in enumerate(robots):
            x,y,vx,vy = robot
            nx = (x+vx+size[0]) % size[0]
            ny = (y+vy+size[1]) % size[1]
            robots[r] = (nx,ny,vx,vy)

        grid = convert_to_grid(robots, size)
      
        # Check for a string which has at least 25 ones in a line
        potential_tree = has_k_consecutive_ones(grid, 25)

        if potential_tree:
            print(f" >> Potential tree at iteration {i+1}!")
            if save_to is not None:
                fname = f"{save_to}/{i}.txt"
                write_grid_to(grid, fname)
                print(f"Written {i+1} to:",fname)

        sleep(delay)

    print(f"Completed iterations {start} to {end}!")




def print_grid(grid):
    for row in grid:
        s = [str(x) for x in row]
        print("".join(s).replace("0", '.'))





if __name__ == '__main__':
    fname = argv[1]
    robots = load(fname)
    size = (101,103)
    if fname == 'example.txt':
        size = (11,7)

        
    # print("Initial Positions:")
    # print_grid(robots_to_grid(robots, size))
    # print()

    p1 = part_one(robots, size)
    print(f"(Part 1) Robot Quadrant Product: {p1}")

    ## Part 2

    # Reload as the first part will have changed the robot positions
    robots = load(fname)

    fdir = f'part_two/{fname}'
    if not exists(fdir):
        makedirs(fdir, exist_ok=True)

    ## Receive user input for iteration range in form "START END"
    response = input("Iteration for part 2? ")    
    splits = response.split(" ")
    start = 0
    if len(splits) == 1:
        end = int(splits[0])
    else:
        start = int(splits[0])
        end = int(splits[1])
    delay_ms = input("Iteration Delay (ms)? ")
    start = max(0, start)
    end = max(start, end)
    delay_ms = (max(0, int(delay_ms)))

    ## Run the simulation for the given number of iterations, saving any with the minimum variance
    check_for_tree(robots, size, start, end, delay_ms, save_to=fdir)