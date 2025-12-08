
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(grid)

adj_vecs = [
    (-1,-1),(-1,0),(-1,1),
    (0,-1),(0,1),
    (1,-1),(1,0),(1,1)
]

def find_movable(grid, selected_pos=None):
    movable = set()
    rows = grid.shape[0]
    cols = grid.shape[1]

    if selected_pos is None:
        selected_pos = set([
            (x,y) for x in range(grid.shape[1])
            for y in range(grid.shape[0])
            if grid[x][y] == '@'
        ])

    for x,y in selected_pos:
        neighbours = [(x+vx,y+vy) for (vx,vy) in adj_vecs]
        n_paper_adj = sum([
            nx >= 0 and nx < cols and ny >= 0 and ny < rows and grid[nx][ny] == '@'
            for nx,ny in neighbours
        ])

        if n_paper_adj < 4:
            movable.add((x,y))

    return movable

def count_movable(grid):
    return len(find_movable(grid))

def count_movable_with_removals(grid):
    try_remove = True
    total_removed = 0

    ## Get the list of positions of rolls of paper
    pos_of_rolls = set([
        (x,y) 
        for x in range(grid.shape[1])
        for y in range(grid.shape[0])
        if grid[x][y] == '@'
    ])

    while try_remove and len(pos_of_rolls) > 0:
        removable = find_movable(grid, pos_of_rolls)
        # print(f"Remove: {removable}")
        try_remove = len(removable) > 0
        total_removed += len(removable)
        pos_of_rolls = pos_of_rolls.difference(removable)
        for x,y in removable:
            grid[x][y] = 'x'

    return total_removed



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    grid = load(fname)
    num_movable = count_movable(grid)
    print(f"Part 1: {num_movable}")

    total_removable = count_movable_with_removals(grid)
    print(f"Part 2: {total_removable}")