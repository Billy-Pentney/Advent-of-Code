
import numpy as np



def load(fname):

    with open(fname, "r") as file:
        grid = [list(l.strip("\n")) for l in file.readlines()]

    return grid

def show(grid):
    for row in grid:
        print("".join(row))


def sign(it):
    if it >= 0:
        return 1
    return -1


def compute_antinodes(grid, p1, p2, part=1):

    rows = len(grid)
    cols = len(grid[0])

    antinodes = []

    p1x,p1y = p1
    p2x,p2y = p2

    ## Compute the gradient from p1 to p2
    dy = p2y-p1y
    dx = p2x-p1x
    d = [dx,dy]
    if d[0] != 0 and d[1] % d[0] == 0:
        # Normalise if possible
        d[0] = d[0] // dx
        d[1] = d[1] // dx
    # print(p1, p2, d)

    ## Compute all (integer) points on the line from p1 to p2 
    candidates = []
    p3 = [p1[0], p1[1]]
    while p3[0] >= 0 and p3[1] >= 0 and p3[0] < cols and p3[1] < rows:
        p3[0] -= d[0]
        p3[1] -= d[1]
    p3[0] += d[0]
    p3[1] += d[1]
    while p3[0] >= 0 and p3[1] >= 0 and p3[0] < cols and p3[1] < rows:
        candidates.append((p3[0],p3[1]))
        p3[0] += d[0]
        p3[1] += d[1]

    # print("Candidates:",candidates)

    if part == 1:
        for x,y in candidates:
            dx1 = abs(p1x-x)
            dy1 = abs(p1y-y)
            dx2 = abs(p2x-x)
            dy2 = abs(p2y-y)

            ## If Part 1, then only include Antinodes at points which are 2x from one point.
            if (2*dx1 == dx2 and 2*dy1 == dy2) or (2*dx2 == dx1 and 2*dy2 == dy1):
                antinodes.append((x,y))
    elif part == 2:
        ## For part 2 we include all nodes on the line from p1 to p2
        antinodes = candidates

    return antinodes



def count_antinodes(grid, part=1):
    rows = len(grid)
    cols = len(grid[0])

    antenna = {}

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] != '.':
                ltr = grid[y][x]
                if ltr not in antenna.keys():
                    antenna[ltr] = []
                antenna[ltr].append((x,y))

    unique_antinodes = set()

    for ltr, positions in antenna.items():
        antinodes_ltr = set()
        n_pos = len(positions)
        
        for i in range(n_pos):
            for j in range(i+1, n_pos):
                p1 = positions[i]
                p2 = positions[j]
                # print(f"Comparing {p1} and {p2}")
                an_12 = compute_antinodes(grid, p1, p2, part=part)
                # an_21 = compute_antinodes(grid, p2, p1)
                antinodes_ltr = antinodes_ltr.union(an_12)
        
        # print(f"{ltr}:", antinodes_ltr)
        for ax,ay in antinodes_ltr:
            if grid[ay][ax] == '.':
                grid[ay][ax] = '#'

        unique_antinodes = unique_antinodes.union(antinodes_ltr)
        
    return len(unique_antinodes)




from sys import argv


if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)
    show(grid)

    n_antinodes = count_antinodes(grid, part=1)
    print(f"(Part 1) Num Antinodes: {n_antinodes}")

    # Reload the grid, to overwrite any changes we made
    grid = load(fname)

    n_antinodes_p2 = count_antinodes(grid, part=2)
    print(f"(Part 2) Num Antinodes: {n_antinodes_p2}")
    