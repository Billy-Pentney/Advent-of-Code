import sys, os
import re
from queue import PriorityQueue
from math import sqrt

import numpy as np


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        for line in file.readlines():
            line_numbers = [int(num) for num in line.replace("\n", "")]
            lines.append(line_numbers)
    return lines

def print_grid(grid, as_string=False):
    for row in grid:
        if as_string:
            print("".join([str(x) for x in row]))
        else:
            print(row)


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
DIRS = [NORTH, EAST, SOUTH, WEST]


def get_enterable_neighbours(grid, curr, last_dir, last_dir_count):
    nbs = []
    x, y = curr
    rows = len(grid)
    cols = len(grid[0])

    if y > 0 and (last_dir_count < 3 or last_dir != NORTH) and last_dir != SOUTH:
        nbs.append(((x, y-1), NORTH))
    if x < cols-1 and (last_dir_count < 3 or last_dir != EAST) and last_dir != WEST:
        nbs.append(((x+1, y), EAST))
    if y < rows-1 and (last_dir_count < 3 or last_dir != SOUTH) and last_dir != NORTH:
        nbs.append(((x, y+1), SOUTH))
    if x > 0 and (last_dir_count < 3 or last_dir != WEST) and last_dir != EAST:
        nbs.append(((x-1, y), WEST))
    
    return nbs




# Calculate square of L2-Norm (square of Pythagorean Distance)
def calc_direct_distance(pos1, pos2):
    return sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)


def last_move_to_symbol(facing):
    if facing == EAST:
        return '>'
    elif facing == NORTH:
        return '^'
    elif facing == SOUTH:
        return 'v'
    elif facing == WEST:
        return '<'
    else:
        return 'X'


INF = 100000000


## Solve Part One
def part_one(fileaddr):
    grid = read_file(fileaddr)

    rows = len(grid)
    cols = len(grid[0])

    # Coordinates in y-x form
    source = (0,0)
    dest = (rows-1,cols-1)

    # min_cost[r][c][d] is the minimum heat-loss in any path from the start to cell at row r, column c, 
    # when entering via direction d (0-3)
    min_cost = np.full((rows,cols,4),INF)

    # moves_used = [[[INF,INF,INF,INF] for x in line] for line in lines]

    frontier = []
    frontier.append((source, ""))

    # frontier = PriorityQueue()
    # frontier.put(((source,"",0)))

    grid_marked = np.array(grid, dtype='str').copy()

    frontier = PriorityQueue()
    frontier.put((calc_direct_distance(source, dest), source, "", source))
    min_cost[source[1]][source[0]] = 0

    print(min_cost)

    visited = np.zeros((rows, cols))
    iters = 0
    max_iters = 10000

    prev = np.zeros((rows,cols,2), dtype='int')

    # while len(frontier) > 0:
    while frontier.not_empty:
        iters += 1
        if iters > max_iters:
            print(f"Exit after {iters} iterations!")
            break

        top = frontier.get()
        _, curr, move_state, prev_cell = top

        cx,cy = curr


        prev[cy][cx] = prev_cell
        print(prev_cell, "~>", curr)

        ## Determine which direction we're facing and how many moves weve used consecutively
        moves_used = len(move_state)
        facing = None
        if moves_used > 0:
            facing = int(move_state[0])
            grid_marked[prev_cell[1]][prev_cell[0]] = '^>v<'[facing]

        print(f"At ({cx},{cy}) from move(s) {move_state} with total cost", min_cost[cy][cx][facing])

        if facing:
            curr_cost = min_cost[cy][cx][facing]
        else:
            curr_cost = min_cost[cy][cx].min()

        if cx == dest[0] and cy == dest[1]:
            break
        
        visited[cy][cx] = 1

        for nb, new_facing in get_enterable_neighbours(grid, curr, facing, moves_used):
            nx,ny = nb
            new_move_state = move_state

            if facing is not None and new_facing == (facing+2)%4:
                continue

            if new_facing == facing:
                ## Moving in same direction
                new_move_state += str(new_facing)
            else:
                new_move_state = str(new_facing)

            # Find the previous lowest-cost to reach this neighbour facing this direction
            old_cost = min_cost[ny][nx][new_facing]
            new_cost = curr_cost + grid[ny][nx]

            # print(old_cost, "vs", new_cost)
            
            if visited[ny][nx] == 0 or new_cost < old_cost:
                new_heuristic = new_cost + calc_direct_distance(nb,dest)
                frontier.put((new_heuristic, nb, new_move_state, (cx,cy)))
                min_cost[ny][nx][new_facing] = new_cost
                visited[ny][nx] = 1

    # print_grid(min_cost)

    dx,dy = dest

    cost_to_goal = min_cost[dy][dx].astype('int')

    print("Goal reachable in:",cost_to_goal)

    ## Reconstruct and show the optimum path

    # vecs = [[0,-1],[1,0],[0,1],[-1,0]]

    # path = []
    # cx,cy = dest
    # while True:
    #     # facing = entered[cy][cx]
    #     # if facing == -1:
    #     #     break
    #     print(cx,cy,facing)
    #     # v = vecs[facing]
    #     px,py = prev[cy][cx]
    #     if px == cx and py == cy:
    #         break
    #     path.append((cx,cy))
    #     cx,cy = px,py
    #     if cx >= cols or cy >= rows or cx < 0 or cy < 0:
    #         break

    # for x,y in path:
    #     grid_marked[y][x] = '-'

    print_grid(grid_marked, as_string=True)
    return cost_to_goal.min()












## Solve Part Two
def part_two(fileaddr):
    return










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
    
