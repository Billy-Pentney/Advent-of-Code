
def load(fname):
    with open(fname, "r") as file:
        grid = [l.strip("\n") for l in file.readlines()]
    return grid

EE = [0,1]
SE = [1,1]
SS = [1,0]
SW = [1,-1]
WW = [0,-1]
NW = [-1,-1]
NN = [-1,0]
NE = [-1,1]


vecs = [EE,SE,SS,SW,WW,NW,NN,NE]

diags = [SE,SW,NE,NW]
## Pairs of opposite diagonals e.g. (SouthEast, NorthWest)
diag_pairs = [[SE,NW], [SW,NE]]


def check_word(grid, d_vec, word, pos):
    x,y = pos
    if grid[y][x] != word[0]:
        return False
    
    n_rows = len(grid)
    n_cols = len(grid[0])

    for i in range(1,len(word)):
        y += d_vec[0]
        x += d_vec[1]
        if x < 0 or y < 0 or x >= n_rows or y >= n_cols:
            return False
        if grid[y][x] != word[i]:
            return False

    return True

def find_instances(grid, letter):
    starts = []
    rows = len(grid)
    cols = len(grid[0])
    ## Find all occurrences of the starting letter
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == letter:
                starts.append((x,y))
    return starts


def search(grid, word):
    starts = find_instances(grid, word[0])

    n_times = 0
    for start in starts:
        # Check each of the 8 directions from this cell
        for vec in vecs:
            if check_word(grid, vec, word, start):
                n_times += 1

    return n_times


def search_for_cross_mas(grid):
    all_as = find_instances(grid, 'A')

    rows = len(grid)
    cols = len(grid[0])
    n_found = 0

    for x,y in all_as:
        n_mas = 0
        # Check each of the 8 directions from this cell
        for up_vec, down_vec in diag_pairs:
            ux, uy = x + up_vec[0], y + up_vec[1]
            vx, vy = x + down_vec[0], y + down_vec[1]

            if ux < 0 or uy < 0 or vx < 0 or vy < 0:
                continue
            if ux >= cols or uy >= rows or vx >= cols or vy >= rows:
                continue

            # print(f"Checking {ux},{uy} to {vx},{vy}")

            s = grid[uy][ux] + grid[vy][vx]
            if s == 'SM' or s == 'MS':
                ## MAS found
                n_mas += 1
            else:
                ## Missing a MAS on the diagonal
                break
        
        ## If we found two diagonals which say "MAS", then we have a cross
        if n_mas == 2:
            n_found += 1
    
    return n_found
                





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)

    word = 'XMAS'

    n_found = search(grid, word)
    print(f"(Part 1) Found: {n_found}")

    n_cross_mas = search_for_cross_mas(grid)
    print(f"(Part 2) Found: {n_cross_mas}")
