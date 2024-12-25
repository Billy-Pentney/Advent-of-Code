
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(grid)

def show(grid):
    for row in grid:
        print("".join(row))

def get_neighbours(grid, curr, depth):
    rows = grid.shape[0]
    cols = grid.shape[1]
    nbs = []
    unique = set()
    queue = [(curr[0],curr[1],0)]

    for i in range(depth):
        new_nbs = []
        ## Get the neighbours of this neighbour
        for cx,cy,_ in queue:
            for vec in vecs:
                nx,ny = cx+vec[0], cy+vec[1]
                if nx >= 0 and ny >= 0 and nx < cols and ny < rows and (nx,ny) not in unique:
                    new_nbs.append((nx,ny,i+1))
                    unique.add((nx,ny))
        nbs.extend(new_nbs)
        queue = new_nbs.copy()

    return set(nbs)
            
        


vecs = [[-1,0],[0,1],[1,0],[0,-1]]

WALL = '#'
FREE = '.'


def find_shortest_to(grid, start, end):
    sx,sy = start
    queue = [(sx,sy,0)]
    min_to = np.full(grid.shape, -1)
    visited = np.zeros(grid.shape)

    # no cost at the start
    min_to[sy][sx] = 0

    ## Standard DFS maintaining the cost when visiting each cell
    while len(queue) > 0:
        x,y,cost = queue[0]
        queue = queue[1:]
        visited[y][x] = 1
        # print(f"{x},{y}, cost={cost}")
        new_cost = cost+1

        # Consider the four adjacent cells, reachable by 1 step
        for nx,ny,_ in get_neighbours(grid, (x,y), 1):
            if grid[ny][nx] == WALL:
                ## Ignore any walls
                continue

            ## Take the minimum case where no skips were used
            if visited[ny][nx] == 0 or new_cost < min_to[ny][nx]:
                min_to[ny][nx] = new_cost
                queue.append((nx,ny,new_cost))
                visited[ny][nx] = 1

    return min_to






def find_num_cheats_with_saving(grid, req_saving=100, max_skips=1):
    start = (0,0)
    end = (0,0)

    ## Locate the start and end positions
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y][x] == 'S':
                start = (x,y)
            elif grid[y][x] == 'E':
                end = (x,y)

    min_to = find_shortest_to(grid, start, end)

    """
        Algorithm:
        1. For each node on the path
        2.     Get all its neighbours which are 2 steps away
        3.     For each 2nd degree nb which is not a wall
        4.          Cost = the shortest path to the start to that cell + the shortest path from the cell to the end
    """

    ## List of points on the shortest no-skip path, in (y,x) notation
    path = np.argwhere(min_to >= 0)
    no_skip_cost = min_to[end[1]][end[0]]
    
    cheats = set()
    cheats_by_saving = dict()

    len_path = len(path)
    printerval = len_path // 10

    for i,(y,x) in enumerate(path):
        if (i+1)%printerval == 0:
            print(f"{i+1}/{len_path}")
        nbs_after_skip = get_neighbours(grid, (x,y), max_skips)
        # print( f"{x},{y}: ... ", nbs_after_skip)
        for nx,ny,d in nbs_after_skip:
            if grid[ny][nx] == FREE or grid[ny][nx] == 'E':
                # Distance from the neighbour to the goal without skips
                nxny_to_goal = no_skip_cost - min_to[ny][nx]

                # Cost with the skip, compared to the cost without
                cost = min_to[y][x] + nxny_to_goal + d
                saving = no_skip_cost - cost

                if saving >= req_saving:
                    cheat_str = f"{(x,y)}->{(nx,ny)}"
                    if saving not in cheats_by_saving.keys():
                        cheats_by_saving[saving] = []
                    cheats_by_saving[saving].append(cheat_str)
                    cheats.add(cheat_str)

    ## Show the number of cheats under each saving amount
    # for saving, chts in sorted(cheats_by_saving.items(), key=lambda x:x[0]):
    #     print(saving,":",len(chts))

    return len(cheats)










from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    grid = load(fname)
    n_cheats = find_num_cheats_with_saving(grid, req_saving=100, max_skips=2)
    print(f"(Part 1) Num Cheats: {n_cheats}")

    n_cheats_2 = find_num_cheats_with_saving(grid, req_saving=100, max_skips=20)
    print(f"(Part 2) Num Cheats: {n_cheats_2}")


