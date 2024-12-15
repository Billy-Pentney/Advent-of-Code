
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        content = file.readlines()

    grid = []
    instructions = ""
    seeing_instructions = False

    for line in content:
        line = line.strip("\n")
        if len(line) == 0:
            seeing_instructions = True
        elif seeing_instructions:
            instructions += line
        else:
            grid.append(list(line))
        
    return np.array(grid), instructions


def show_grid(grid):
    for row in grid:
        print("".join(row))


def find_start(grid, start='@'):
    """ Locate the starting position (denoted by '@') in the grid and return its coordinates. """
    rows = grid.shape[0]
    cols = grid.shape[1]
    cx,cy = 0,0 
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == start:
                cx,cy = x,y
                break
    return cx,cy



def calc_gps(grid, box_sym='O'):
    """
        Calculate the GPS score of each box in the grid and return the sum.
    """
    total_gps = 0
    rows = grid.shape[0]
    cols = grid.shape[1]
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == box_sym:
                gps = 100 * y + x
                total_gps += gps

    return total_gps



## Converting symbols to directions and vectors
move_to_dir = {'^': 0, '>': 1, 'v': 2, '<': 3}
vecs = [(0,-1), (1,0), (0,1), (-1,0)]




def part_one(grid, moves):

    rows = grid.shape[0]
    cols = grid.shape[1]

    ## Find the starting position (denoted by '@')
    cx,cy = find_start(grid)

    for move in moves:
        d = move_to_dir[move]
        vec = vecs[d]

        ## Check if the robot can move
        tx,ty = cx+vec[0],cy+vec[1]
        can_move = False
        ## Find the first cell ahead of the robot which we can "push" into
        while tx >= 0 and tx < cols and ty >= 0 and ty < rows:
            # print(f"Checking {tx},{ty}")
            if grid[ty][tx] == '.':
                can_move = True
                break
            elif grid[ty][tx] == '#':
                break
            tx += vec[0]
            ty += vec[1]

        ## Robot can't move, so we skip this instruction
        if not can_move:
            continue

        ## Otherwise, push all boxes ahead of it by 1 square
        ## This is equivalent to moving the first box to (tx,ty) and updating the robot position

        ## The next cell after the robot
        nx,ny = cx+vec[0], cy+vec[1]

        if grid[ny][nx] == 'O':
            ## Push the obstacle(s) into the free space
            grid[ty][tx] = 'O'
        
        ## Move the robot forward 1 space
        grid[ny][nx] = '@'
        grid[cy][cx] = '.'
        cx = nx
        cy = ny

    ## Calculate the score of the GPS boxes
    ## GPS = 100 times its distance from the top edge of the map plus its distance from the left edge of the map

    return calc_gps(grid)



def expand_grid(grid):
    rows = grid.shape[0]
    cols = grid.shape[1]
    new_grid = np.full((rows, cols*2), '.')

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == '#':
                new_grid[y,2*x] = '#'
                new_grid[y,2*x+1] = '#'
            elif grid[y][x] == 'O':
                new_grid[y,2*x] = '['
                new_grid[y,2*x+1] = ']'
            elif grid[y][x] == '@':
                new_grid[y,2*x] = '@'

            ## Don't need to duplicate '.' as the array is filled

    return new_grid




def part_two(grid, moves):
    cx,cy = find_start(grid)

    for move in moves:
        d = move_to_dir[move]
        vec = vecs[d]

        # print(f"Move: {move}")

        ## Check if the robot can move
        pushing = [(cx,cy)]

        can_move = True

        i = 0
        while i < len(pushing):
            tx,ty = pushing[i]
            nx,ny = tx+vec[0],ty+vec[1] 

            ## If this cell cannot move due to a wall
            if grid[ny][nx] == '#':
                can_move = False
                break

            # Check what we are pushing into
            if d % 2 == 0:
                ## Pushing up
                if grid[ny][nx] == '[':
                    pushing.append((nx,ny))
                    pushing.append((nx+1,ny))
                ## Down
                elif grid[ny][nx] == ']':
                    pushing.append((nx-1,ny))
                    pushing.append((nx,ny))

            elif grid[ny][nx] != '.':
                ## Pushing left or right
                pushing.append((nx,ny))
                pushing.append((nx+vec[0],ny+vec[1]))
                i += 1

            i += 1
    
        if not can_move:
            # print(f"Can't move in direction {move}")
            continue

        ## Drop duplicates
        moved = set()

        ## Push the boxes
        for i in range(len(pushing)-1,0,-1):
            ax,ay = pushing[i]
            ## Skip any boxes which have already moved
            if pushing[i] in moved:
                continue
            bx,by = ax+vec[0],ay+vec[1]
            # print(f"{ax},{ay} ~> {bx},{by}")
            grid[by][bx] = grid[ay][ax]
            grid[ay][ax] = '.'
            moved.add(pushing[i])

        ## Move the robot forward 1 space
        grid[cy+vec[1]][cx+vec[0]] = '@'
        grid[cy][cx] = '.'
        cx = cx+vec[0]
        cy = cy+vec[1]

        ## Show the grid if we moved at least one box
        # if len(pushing) > 1:
        #     show_grid(grid)
        #     print()

    ## Show the final grid after all moves
    show_grid(grid)
    print()

    ## Calculate the score of the GPS boxes (left side only)
    return calc_gps(grid, '[')





from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    grid, moves = load(fname)

    print("*"*30, "PART 1", "*"*30)
    show_grid(grid)
    total_gps = part_one(grid, moves)
    print(f"(Part 1) Total GPS: {total_gps}")


    print()
    print("*"*30, "PART 2", "*"*30)
    exp_grid = expand_grid(grid)
    # show_grid(exp_grid)
    p2 = part_two(exp_grid, moves)
    print(f"(Part 2) Total GPS: {p2}")