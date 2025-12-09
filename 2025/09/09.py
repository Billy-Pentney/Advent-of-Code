
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        coords = [
            [int(x) for x in row.strip("\n").split(",")]
            for row in file.readlines()
        ]

    return coords

def construct_grid(coords):
    max_vals = np.max(coords, axis=0)
    grid = np.zeros((max_vals[1]+2, max_vals[0]+2))
    for (x,y) in coords:
        grid[y,x] = 1
    return grid


def display_grid(grid):
    n_rows = grid.shape[0]
    n_cols = grid.shape[1]

    for y in range(n_rows):
        line = ""
        for x in range(n_cols):
            if grid[y,x] == 1:
                line += "#"
            else:
                line += "."

        print(line)

def find_largest_rectangle(coords):
    max_area = 0
    chosen = (0,1)
    for i,pt1 in enumerate(coords):
        for j,pt2 in enumerate(coords[i+1:]):
            x1 = min(pt2[0],pt1[0])
            y1 = min(pt2[1],pt1[1])
            x2 = max(pt2[0],pt1[0])
            y2 = max(pt2[1],pt1[1])
            area = (1+x2-x1)*(1+y2-y1)
            if area > max_area:
                max_area = area
                chosen = (i,i+j)

    print(coords[chosen[0]], coords[chosen[1]])

    return max_area




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    coords = load(fname)
    # grid = construct_grid(coords)
    # display_grid(grid)

    largest_rect_area = find_largest_rectangle(coords)
    print("Part 1:", largest_rect_area)