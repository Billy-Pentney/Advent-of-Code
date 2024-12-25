
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(grid)


def get_neighbours(grid, x, y):
    nbs = [(x+1,y), (x,y+1), (x-1,y), (x,y-1)]
    return [(x_,y_) for (x_,y_) in nbs if x_>=0 and y>=0 and x<len(grid[0]) and y<len(grid)]


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

dirs = {
    NORTH: [0,-1],
    EAST: [1,0],
    SOUTH: [0,1],
    WEST: [-1,0]
}

def part_one(grid):
    start = None
    end = None
    rows = len(grid)
    cols = len(grid[0])

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 'S':
                start = (x,y)
            elif grid[y][x] == 'E':
                end = (x,y)

    print(f"Start: {start}, End: {end}")

    queue = [(start, EAST)]
    ## min_cost[y][x][d] is the minimum known cost to enter cell (x,y) while facing direction d
    min_cost = np.full((rows, cols, 4), -1)
    min_cost[start[1]][start[0]] = 0
    # from_cell = np.zeros((rows,cols,2), dtype='int')
    # from_cell[start[1]][start[0]] = start

    ## BFS
    while len(queue) > 0:
        (cx,cy),curr_dir = queue[0]
        queue = queue[1:]
        
        cost = min_cost[cy][cx][curr_dir]

        if cost < 0:
            ## Ignore any directions from which we didn't enter this cell
            continue

        for exit_dir, vec in dirs.items():
            nx,ny = cx+vec[0],cy+vec[1]
            if grid[ny][nx] == '#':
                ## Cannot enter a wall
                continue
            
            new_cost = cost+1
            if exit_dir != curr_dir:
                ## Gain 1000 for each 90 degree rotation
                clockwise = abs(exit_dir-curr_dir) ## d >= curr_dir
                counter = 4 - curr_dir + exit_dir  ## d < curr_dir
                # print(f"{curr_dir} -> {d} has clockwise = {clockwise}, counter = {counter}")
                new_cost += 1000 * min(clockwise, counter)
            
            if min_cost[ny][nx][exit_dir] < 0 or new_cost < min_cost[ny][nx][exit_dir]:
                # print(f"Cost to reach {nx},{ny} facing {list('NESW')[d]} is: {new_cost}")
                queue.append(((nx,ny),exit_dir)) 
                min_cost[ny][nx][exit_dir] = new_cost


    goal_cost = min_cost[end[1]][end[0]]
    print(goal_cost)
    # Take the minimum over the directions which reached the goal
    min_goal_cost = goal_cost[goal_cost >= 0].min()
    return min_goal_cost




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    grid = load(fname)

    min_score = part_one(grid)
    print(f"(Part 1) Minimum Score: {min_score}")
