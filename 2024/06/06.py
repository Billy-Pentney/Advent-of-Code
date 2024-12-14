
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        map = [list(line.strip("\n")) for line in file.readlines()]

    return map



NORTH = [-1,0]
SOUTH = [1,0]
EAST = [0,1]
WEST = [0,-1]

dirs = [NORTH, EAST, SOUTH, WEST]


UP = '^'
RIGHT = '>'
DOWN = 'v'
LEFT = '<'
OBSTACLE = '#'
BLOCKER = 'O'
VISITED = 'X'

def part_one(grid):
    rows = len(grid)
    cols = len(grid[0])

    X,Y,d = 0,0,0
    seen = np.zeros((rows, cols, 4))

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == UP:
                X,Y,d = x,y,0
            elif grid[y][x] == RIGHT:
                X,Y,d = x,y,1
            elif grid[y][x] == DOWN:
                X,Y,d = x,y,2
            elif grid[y][x] == LEFT:
                X,Y,d = x,y,d


    n_blockers = 0

    while True:
        vec = dirs[d]
        nx, ny = X + vec[1], Y + vec[0]
        seen[Y][X][d] = 1

        if grid[Y][X] != BLOCKER:
            grid[Y][X] = VISITED

        ## If about to leave the map, stop
        if nx < 0 or nx >= cols or ny < 0 or ny >= rows:
            break

        if grid[ny][nx] == OBSTACLE:
            # Rotate 90 degrees clockwise
            d = (d+1)%4
            seen[Y][X][d] = 1

        else:

            ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ PART TWO

            # If there were an obstacle, would it create a cycle?
            d_ = (d+1)%4
            v_ = dirs[d_]
            aX, aY = X+v_[1], Y+v_[0]

            ## Make a copy for this exploration, so we don't affect the actual
            seen_temp = seen.copy()

            ## Does this rejoin an existing path we've taken?
            ## We check until we leave the map or revisit a cell.
            while aX >= 0 and aY >= 0 and aX < cols and aY < rows:
                if seen_temp[aY][aX][d_] > 0:
                    ## Already visited this cell from this direction
                    n_blockers += 1
                    print(f"Blocker at {nx},{ny}")
                    grid[ny][nx] = BLOCKER
                    break
            
                seen_temp[aY][aX][d_] = 2
                
                ## Check if we can proceed to the next cell
                bX,bY = aX+v_[1], aY+v_[0]
                if bX >= 0 and bY >= 0 and bX < cols and bY < rows:
                    if grid[bY][bX] == OBSTACLE:
                        # Rotate 90
                        d_ = (d_+1)%4
                        v_ = dirs[d_]

                    aX += v_[1]
                    aY += v_[0]

                else:
                    break

             

            ## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            # Step forward
            X,Y = nx,ny
        

    visited = (seen == 1).any(axis=2).astype(int)
    n_unique_visited = np.sum(visited, dtype='int')


    for row in grid:
        print("".join(row))
        
    return n_unique_visited, n_blockers








from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid_map = load(fname)

    n_unique, n_blockers = part_one(grid_map)
    print(f"(Part 1) Num Cells: {n_unique}")
    print(f"(Part 2) Num Blocker positions: {n_blockers}")

