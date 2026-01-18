
def load(fname):
    with open(fname, "r") as file:
        lines = file.readlines()

    lands = []
    for line in lines:
        coords = line.strip("\n").split(",")
        if len(coords) == 2:
            x = int(coords[0])
            y = int(coords[1])
            lands.append((x,y))

    return lands


import numpy as np

def print_grid(grid):
    for row in grid:
        print("".join(row))

def get_neighbours(x,y,grid_size):
    rows,cols = grid_size
    nbs = []
    if x > 0:
        nbs.append((x-1,y))
    if x < cols-1:
        nbs.append((x+1,y))
    if y > 0 :
        nbs.append((x,y-1))
    if y < rows-1:
        nbs.append((x,y+1))
    return nbs


def dfs(grid, grid_size, goal, show_grid=True):
    queue = []
    queue.append((0,0))

    min_to = np.full(grid_size, -1)
    min_to[0][0] = 0
    pred = np.zeros([grid_size[0], grid_size[1], 2], dtype='int')

    while len(queue) > 0:
        cx,cy = queue[0]
        queue = queue[1:]

        if cx == goal[0] and cy == goal[1]:
            ## Goal reached
            break

        nbs = get_neighbours(cx, cy, grid_size)
        for nx,ny in nbs:
            if grid[ny][nx] == '#':
                continue    ## Blocked
            if min_to[ny][nx] < 0:
                min_to[ny][nx] = min_to[cy][cx] + 1
                queue.append((nx,ny))
                pred[ny][nx] = (cx,cy)
            elif min_to[cy][cx]+1 < min_to[ny][nx]:
                min_to[ny][nx] = min_to[cy][cx] + 1
                queue.append((nx,ny))
                pred[ny][nx] = (cx,cy)

    ## Reconstruct the shortest path
    curr = goal
    while curr[0] != 0 or curr[1] != 0:
        grid[curr[1]][curr[0]] = 'O'
        curr = pred[curr[1], curr[0], :]
    
    if show_grid:
        print_grid(grid)
        
    return min_to[goal[1]][goal[0]]



def part_one(lands, grid_size, n_sim=1024):

    grid = np.full(grid_size, '.')
    for i in range(min(n_sim, len(lands))):
        x,y = lands[i]
        grid[y][x] = '#'
    
    goal = (grid_size[1]-1, grid_size[0]-1)
    return dfs(grid, grid_size, goal)    




def part_two(lands, grid_size, n_steps=1024):

    grid = np.full(grid_size, '.')
    ## Simulate the first k steps
    for i in range(min(n_steps, len(lands))):
        x,y = lands[i]
        grid[y][x] = '#'

    goal = (grid_size[1]-1, grid_size[0]-1)

    ## Brute-Force, simulate landings and check if DFS is possible after each one
    while i < len(lands):
        x,y = lands[i]
        grid[y][x] = '#'
        print(f"Land at: {x},{y}")

        dfs_result = dfs(grid.copy(), grid_size, goal, show_grid=False)
        if dfs_result == -1:
            ## Stop when we can no longer solve the maze
            return (x,y)
        
        i+=1
    
    return (0,0)





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    landing = load(fname)

    grid_size = (71,71)
    n_steps = 1024

    ## Alternative setup for the example (small grid)
    if fname == 'example.txt':
        grid_size = (7,7)
        n_steps = 12
    
    goal = part_one(landing, grid_size, n_steps)
    print(f"(Part 1) Steps to goal: {goal}")

    first_closed = part_two(landing, grid_size, n_steps)
    print(f"(Part 2) All paths closed by: {first_closed}")
