
import regex as re
import numpy as np

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


def robots_to_grid(robots, size):
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
            x_ = x+vx
            y_ = y+vy

            if x_ < 0:
                x_ += cols
            elif x_ >= cols:
                x_ = x_ % cols
            if y_ < 0:
                y_ += rows
            elif y_ >= rows:
                y_ = y_ % rows
            
            robots[r] = (x_,y_,vx,vy)

    hc = cols//2
    hr = rows//2
    
    quadrants = [
        (0, hr, 0, hc),         ## Upper-left
        (rows-hr, rows, 0, hc), ## Lower-left
        (0, hr, cols-hc, cols), ## Upper-right
        (rows-hr, rows, cols-hc, cols)  ## Lower-right
    ]

    grid = robots_to_grid(robots, size)
    # print_grid(grid)
    quad_counts = [0,0,0,0]

    for i,quad in enumerate(quadrants):
        y1,y2,x1,x2 = quad
        quad_counts[i] = np.sum(grid[y1:y2,x1:x2])
        # print(f"Quad {i+1} is:")
        # print_grid(grid[y1:y2,x1:x2])
        # print(f">> has {quad_counts[i]} robots")


    # print(f"Quadrant counts: {quad_counts}")
    return np.product(quad_counts)


from time import sleep

def write_grid_to(grid, fname):
    with open(fname, "w") as file:
        str_grid = ["".join(list(map(str, row)))+"\n" for row in grid]
        str_grid = [row.replace('0', '.') for row in str_grid]
        file.writelines(str_grid)


def neighbours(x, y, rows, cols):
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


def check_for_box(robots, grid):
    rows = grid.shape[0]
    cols = grid.shape[1]


    for x,y,_,_ in robots:
        seen = np.zeros(grid.shape)
        queue = [(x,y)]

        ## BFS to find a loop
        while len(queue) > 0:
            cx,cy = queue[0]
            queue = queue[1:]
            ## Found a loop
            if seen[cy][cx] == 1:
                return True
            
            seen[cy][cx] = 1

            for nb in neighbours(cx, cy, rows, cols):
                if grid[cy][cx] > 0 and seen[cy][cx] == 0:
                    queue.append(nb)


    return False


def run_iterations(robots, size, start, end, delay_ms=1000, save_to=None):
    # grid = robots_to_grid(robots, size)

    rows = size[1]
    cols = size[0]

    for r,robot in enumerate(robots):
        x,y,vx,vy = robot
        nx = ((start+1) * (x+vx)) % size[0]
        ny = ((start+1) * (y+vy)) % size[1]
        robots[r] = (nx,ny,vx,vy)

    min_var = None

    for i in range(start, end):
        if i % 1000 == 0:
            print(f"ITERATION {i+1}")

        for r,robot in enumerate(robots):
            x,y,vx,vy = robot
            nx = (x+vx+size[0]) % size[0]
            ny = (y+vy+size[1]) % size[1]
            robots[r] = (nx,ny,vx,vy)

        grid = robots_to_grid(robots, size)
      
        var_x = np.std(np.array(robots)[:,0])
        var_y = np.std(np.array(robots)[:,1])
        var = var_x * var_y

        if min_var is None or var < min_var:
            min_var = var
            print(f"{i+1}: {min_var}")
            print_grid(grid)
            if save_to is not None:
                fname = f"{save_to}/{i}.txt"
                write_grid_to(grid, fname)

        sleep(delay_ms/1000.0)

    print(f"Completed iterations {start} to {end}!")


def print_grid(grid):
    for row in grid:
        s = [str(x) for x in row]
        print("".join(s).replace("0", '.'))


from sys import argv
from os.path import exists
from os import makedirs

if __name__ == '__main__':
    fname = argv[1]
    robots = load(fname)
    size = (101,103)
    if fname == 'example.txt':
        size = (11,7)

        
    # print("Initial Positions:")
    # print_grid(robots_to_grid(robots, size))
    # print()
    # p1 = part_one(robots,size)
    # print(f"(Part 1) Robot Quadrant Product: {p1}")

    ## Part 2
    fdir = f'part_two/{fname}'
    if not exists(fdir):
        makedirs(fdir, exist_ok=True)

    ## User input for iteration range in form "START END"
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
    run_iterations(robots, size, start, end, delay_ms, save_to=fdir)