
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        map = [list(line.strip("\n")) for line in file.readlines()]

    return map



NORTH = [0,-1]
SOUTH = [0,1]
EAST = [1,0]
WEST = [-1,0]

dirs = [NORTH, EAST, SOUTH, WEST]


UP = '^'
RIGHT = '>'
DOWN = 'v'
LEFT = '<'
OBSTACLE = '#'
BLOCKER = 'O'
VISITED = 'X'


def check_for_loop(grid, state):
    """
        Checks if the movement of the guard from the given state leads to an infinite loop.
        State is a 3-tuple (x,y,d) where (x,y) is the coordinates in the grid and d is the direction (0=NORTH,1=EAST,2=SOUTH,3=WEST).
        Returns true if a loop is found.
    """
    x,y,d = state
    
    rows = len(grid)
    cols = len(grid[0])
    visited = np.zeros((rows,cols,4), dtype='int')

    while x >= 0 and y >= 0 and x < cols and y < rows:
        if visited[x,y,d] == 1:
            return True
        
        visited[x,y,d] = 1

        vec = dirs[d]
        nx,ny = x+vec[0],y+vec[1]

        if nx >= 0 and ny >= 0 and nx < cols and ny < rows:
            if grid[ny][nx] == OBSTACLE or grid[ny][nx] == BLOCKER:
                # Turn right 90 degrees
                d = (d+1)%4
            else:
                x,y = nx,ny
                # Move and keep same direction
        else:
            ## About to leave the map
            # print(f" > Leaving map at {(nx,ny)}")
            return False

    # print(f" > Left map at {(x,y)}")
    return False






def solve_both_parts(grid):
    rows = len(grid)
    cols = len(grid[0])

    cx,cy,d = 0,0,0
    seen = np.zeros((rows, cols, 4))

    # Find the starting position and direction
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == UP:
                cx,cy,d = x,y,0
            elif grid[y][x] == RIGHT:
                cx,cy,d = x,y,1
            elif grid[y][x] == DOWN:
                cx,cy,d = x,y,2
            elif grid[y][x] == LEFT:
                cx,cy,d = x,y,3


    ## Indicates if the given cell is a blocker (-1 = not checked, 0 = no, 1 = yes)
    blockers = np.full((rows,cols), -1, dtype='int')
    n_blockers = 0

    ## Follow the path
    while True:
        vec = dirs[d]
        nx, ny = cx + vec[0], cy + vec[1]
        seen[cy][cx][d] = 1

        ## If about to leave the map, stop
        if nx < 0 or nx >= cols or ny < 0 or ny >= rows:
            break

        if grid[ny][nx] == OBSTACLE:
            # Rotate 90 degrees clockwise
            d = (d+1)%4
            seen[cy][cx][d] = 1

        else:

            ## ~~~~~~~~~ PART TWO - Check if this is a blocker ###

            if blockers[ny][nx] < 0:
                ## Suppose we place an obstacle at (nx,ny)
                grid2 = np.array(grid)
                grid2[ny][nx] = BLOCKER
                grid2[cy][cx] = 'M'
 
                # print(f"Checking for blocker at... ({nx},{ny})")
                # If there were an obstacle, would it create a cycle?
                creates_cycle = check_for_loop(grid2, (cx,cy,d))

                if creates_cycle:
                    blockers[ny][nx] = 1
                    n_blockers += 1
                    ## Don't overwrite the grid here otherwise we impact other cells.
                else:
                    blockers[ny][nx] = 0

            ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # Step forward
            cx,cy = nx,ny
        
    visited = (seen == 1).any(axis=2).astype(int)
    n_unique_visited = np.sum(visited, dtype='int')

    # Draw the blockers on the grid
    for by,bx in np.argwhere(blockers == 1):
        grid[by][bx] = BLOCKER

    for row in grid:
        print("".join(row))
        
    return n_unique_visited, n_blockers







from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid_map = load(fname)

    n_unique, n_blockers = solve_both_parts(grid_map)
    print(f"(Part 1) Num Cells: {n_unique}")
    print(f"(Part 2) Num Blocker positions: {n_blockers}")

