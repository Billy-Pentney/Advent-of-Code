
import numpy as np
# import regex as re
# from collections import defaultdict
from queue import PriorityQueue, Queue

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    designer_num = int(lines[0].strip())
    x,y = lines[1].split(",")
    target = (int(x),int(y))
    return designer_num, target


FREE = 0
WALL = 1
PATH = 2
START = 3
GOAL = 4

state_to_sym = {
    FREE: '.',
    WALL: '#',
    PATH: 'O',
    START: 'S',
    GOAL: 'G'
}

def show(grid: np.array):
    print()
    for y in range(grid.shape[0]):
        line = ""
        for x in range(grid.shape[1]):
            # line += " " + state_to_sym[grid[y][x]] + " "
            line += state_to_sym[grid[y][x]]
        print(line)
    print()

cell_cache = {}

def compute_cell(designer_num, x, y):
    # Find x*x + 3*x + 2*x*y + y + y*y.
    # Add the office designer's favorite number (your puzzle input).
    # Find the binary representation of that sum; count the number of bits that are 1.
    #     If the number of bits that are 1 is even, it's an open space.
    #     If the number of bits that are 1 is odd, it's a wall.

    if (x,y) not in cell_cache:
        res = x*(3+x) + y*(y+1) + 2*x*y + designer_num
        n_ones = 0
        while res > 0:
            n_ones += res % 2
            res = res // 2
        ## Return 1 if a wall, or 0 otherwise
        cell_cache[(x,y)] = n_ones % 2 == 1

    return cell_cache[(x,y)]


def solve_path_through_grid(grid_shape, designer_num, start, target):
    path = find_path(grid_shape, designer_num, start, target)

    grid = np.zeros(grid_shape, dtype=int)
    for y in range(grid_shape[0]):
        for x in range(grid_shape[1]):
            grid[y,x] = compute_cell(designer_num, x, y)

    path_len = 0
    if path is not None:
        for x,y in path:
            grid[y][x] = PATH
        path_len = len(path)

    grid[start[1],start[0]] = START
    grid[target[1],target[0]] = GOAL
    show(grid)
    return path_len

vecs = [[0,1],[1,0],[0,-1],[-1,0]]

def calc_heuristic(start,end):
    return np.linalg.norm(np.array(start)-np.array(end))

def find_path(grid_shape, designer_num, start, goal):
    """
    A*-style exploration to find the shortest-path from start to goal in the grid of the given shape.
    
    :param grid_shape: The size (h,w) of the grid.
    :param designer_num: The number used by compute_cell to determine if a cell is a wall or free.
    :param start: The (x,y) coordinates of the starting cell
    :param goal: The (x,y) coordinates of the goal cell
    """
    shortest_path_to = {}

    frontier = PriorityQueue()
    x,y = start[0],start[1]
    h = calc_heuristic((x,y), goal)
    frontier.put((h,x,y,0))
    shortest_path_to[(x,y)] = 0
    prev = {(x,y): None}

    n_rows = grid_shape[0]
    n_cols = grid_shape[1]

    while not frontier.empty():
        h,x,y,d = frontier.get()
        print(x,y)
        if (x,y) == goal:
            break

        for v in vecs:
            nx,ny = x+v[0], y+v[1]
            if nx < 0 or ny < 0 or nx >= n_rows or ny >= n_cols:
                continue
            if compute_cell(designer_num, nx, ny) == WALL:
                continue
            
            dist = d + 1
            h = dist+calc_heuristic((nx,ny), goal)
            if (nx,ny) not in shortest_path_to or dist < shortest_path_to[(nx,ny)]:
                shortest_path_to[(nx,ny)] = dist
                prev[(nx,ny)] = (x,y)
                frontier.put((h,nx,ny,dist))

    ## Generate the sequence of cells visited (for visualisation)
    if goal in shortest_path_to:
        path = []
        curr = goal
        while prev[curr] is not None:
            path.append(curr)
            curr = prev[curr]
        path.reverse()
        return path
    
    return None

def explore_in_finite_steps(grid_shape, designer_num, start, n_steps):
    queue = Queue()
    queue.put((start[0], start[1], 0))
    seen = set()
    seen.add(start)

    n_rows = grid_shape[0]
    n_cols = grid_shape[1]

    while not queue.empty():
        x,y,d = queue.get()
        seen.add((x,y))

        if d == n_steps:
            ## If we've run out of steps, stop
            continue

        for v in vecs:
            nx,ny = x+v[0], y+v[1]
            if nx < 0 or ny < 0 or nx >= n_rows or ny >= n_cols:
                continue
            if compute_cell(designer_num, nx, ny) == WALL:
                continue

            if (nx,ny) not in seen:
                queue.put((nx,ny,d+1))

    return len(seen)




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    designer_num, target = load(fname)
    print(designer_num, target)

    width = target[0]
    height = target[1]
    ## Add one so that we can reach the target
    side = max(width, height)+1
    shape = (side,side)
    start = (1,1)

    min_steps = solve_path_through_grid(shape, designer_num, start, target)
    print("Part one:", min_steps)

    max_steps = 50
    max_explorable = explore_in_finite_steps(shape, designer_num, start, max_steps)
    print("Part two:", max_explorable)
