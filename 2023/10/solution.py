import sys, os
# import re
from queue import PriorityQueue, Queue
import numpy as np

class Grid():
    def __init__(self, n_rows, n_cols, fill_char='.'):
        self.size = (n_rows, n_cols)
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [list(fill_char * n_cols) for _ in range(n_rows)]
        self.start_pos = None
        self.border = []

    def show(self):
        for row in self.grid:
            print("".join(row))
    
    def set(self, x, y, value):
        self.grid[y][x] = value

    def get(self, x, y):
        return self.grid[y][x]
    
    def set_border(self, border):
        self.border = border

    def show_border(self):
        lines = [list("." * self.n_cols) for _ in range(self.n_rows)]
        for x,y in self.border:
            lines[y][x] = self.grid[y][x]
        for line in lines:
            print("".join(line))

    def save(self, filename, border_only=False):
        lines = [list("." * self.n_cols) for _ in range(self.n_rows)]
        if border_only:
            for x,y in self.border:
                lines[y][x] = self.grid[y][x]
        else:
            lines = self.grid
        
        with open(filename, "w", encoding='utf-8') as file:
            file.writelines(["".join(it)+"\n" for it in lines])
        print(f"Saved to: {filename}")
        

def make_grid_from_text(lines):
    n_rows = len(lines)+2
    n_cols = len(lines[0])+2
    g = Grid(n_rows, n_cols)
    for y,row in enumerate(lines):
        for x,cell in enumerate(row):
            g.set(x+1,y+1,cell)
            if cell == 'S':
                g.start_pos = (x+1,y+1)
    return g


def copy_grid(other: Grid):
    newgrid = Grid(other.n_rows, other.n_cols)
    for y in range(other.n_rows):
        for x in range(other.n_cols):
            newgrid.set(x,y,other.get(x,y))
    return newgrid


# Cardinal movement
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


## Symbols
#   | = vertical pipe connecting north and south.
#   - = horizontal pipe connecting east and west.
#   L = 90-degree bend connecting north and east.
#   J = 90-degree bend connecting north and west.
#   7 = 90-degree bend connecting south and west.
#   F = 90-degree bend connecting south and east.
#   . = no pipe in this tile.
#   S = starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
VPIPE = '│'
HPIPE = '─'
LD = '┐'
LU = '┘'
RD = '┌'
RU = '└'


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r", encoding='utf-8') as file:
        lines = [l.strip("\n") for l in file.readlines()]
    
    clean_lines = []
    for line in lines:
        if len(line) == 0:
            break
        line = line.replace("F", RD)
        line = line.replace("J", LU)
        line = line.replace("L", RU)
        line = line.replace("7", LD)
        line = line.replace("-", HPIPE)
        line = line.replace("|", VPIPE)
        clean_lines.append(list(line))

    grid = make_grid_from_text(clean_lines)
    return grid


def get_enterable_neighbours(grid, start_pos, prev_pos=(-1,-1)):
    """
    Given a position in a grid which falls on the path, return a list of the neighbouring cells
    which are also on the path, along with the direction in which we should move.
    """
    nbs = []
    (col, row) = start_pos
    moves = list("0000")

    # Move North from current
    if row > 0 and grid.get(col, row-1) in [VPIPE, LD, RD]:
        nbs.append((col,row-1))
        moves[UP] = 1
    # Move East from current
    if col < grid.n_cols-1 and grid.get(col+1, row) in [HPIPE, LU, LD]:
        nbs.append((col+1,row))
        moves[RIGHT] = 1
    # Move South from current
    if row < grid.n_rows-1 and grid.get(col,row+1) in [VPIPE, LU, RU]:
        nbs.append((col,row+1))
        moves[DOWN] = 1
    # Move West from current
    if col > 0 and grid.get(col-1,row) in [HPIPE, RU, RD]:
        nbs.append((col-1,row))
        moves[LEFT] = 1
    
    new_nbs = [nb for nb in nbs if nb != prev_pos]
    return new_nbs, moves



def get_next_cell_on_path(curr, curr_pos, prev_pos=(-1,-1)):
    """
    Deduce the coordinates of the next two neighbours on the path, based on the shape of the current symbol.
    E.g. if curr is 'F', then we look one cell to the right and one cell below.
    """

    (col, row) = curr_pos
    candidates = []

    if curr == VPIPE:   
        candidates = [(col,row-1), (col,row+1)]
    elif curr == HPIPE: 
        candidates = [(col-1,row), (col+1,row)]
    elif curr == RD:    
        candidates = [(col+1,row), (col,row+1)]
    elif curr == LD:    
        candidates = [(col-1,row), (col,row+1)]
    elif curr == RU:    
        candidates = [(col+1,row), (col,row-1)]
    elif curr == LU:    
        candidates = [(col-1,row), (col,row-1)]        

    return [nb for nb in candidates if nb != prev_pos]


def find_character_from_moves(moves):
    if moves[RIGHT]:
        if moves[DOWN]: return RD
        elif moves[UP]: return RU
        else:           return HPIPE
    elif moves[LEFT]:
        if moves[DOWN]: return LD
        elif moves[UP]: return LU
    else:
        return VPIPE
    
    return None



def run_dfs_on_path(grid: Grid, start_pos: tuple):
    nbs, moves = get_enterable_neighbours(grid, start_pos)
    # For each cell in the loop, store its shortest distance to S
    dist_map = { start_pos: 0 }

    # Stores tuples of (distance, cell, previous cell) which should be considered by DFS
    frontier = PriorityQueue()
    for nx,ny in nbs:
        frontier.put((1, (nx,ny), start_pos))

    start_char = find_character_from_moves(moves)
    # print("Start character is:", start_char)

    sx,sy = start_pos
    grid.set(sx, sy, start_char)

    while not frontier.empty():
        # Remove the first element in the queue
        (d, curr, prev) = frontier.get()

        # New cell (not seen in loop)
        if curr not in dist_map.keys():
            dist_map[curr] = d
        else:
            break
        
        cx,cy = curr[0],curr[1]
        curr_sym = grid.get(cx,cy)
        for x,y in get_next_cell_on_path(curr_sym, curr, prev):
            frontier.put((d+1, (x,y), curr))

    return dist_map


def part_one(fileaddr):
    grid = read_file(fileaddr)
    print("Start:", grid.start_pos)
    dist_map = run_dfs_on_path(grid, grid.start_pos)
    grid.set_border(list(dist_map.keys()))
    grid.show_border() 
    return max(dist_map.values())


FOUR_VECS = [[0,1],[1,0],[0,-1],[-1,0]]

def is_point_in_loop(point, grid_size, border):
    wall_seen = [0,0,0,0]
    n_rows = grid_size[0]
    n_cols = grid_size[1]

    if point in border:
        return True
    
    sx,sy = point

    ## Check each cardinal direction
    for d in range(4):
        x,y = sx,sy
        v = FOUR_VECS[d]
        wall_seen_here = False
        ## Step forward until we see a cell which is in the border (or leave the grid)
        while y > 0 and y < n_rows-1 and x > 0 and x < n_cols-1:
            x += v[0]
            y += v[1]
            wall_seen_here = (x,y) in border
            if wall_seen_here:
                break
        if wall_seen_here:
            wall_seen[d] = 1

    # print("Walls seen:", wall_seen)
    ## Inside iff all four sides have a wall
    return sum(wall_seen) == 4

def find_inside_outside_2(path, grid_size):
    n_rows = grid_size[0]
    n_cols = grid_size[1]

    inside = set()
    for y in range(n_rows):
        for x in range(n_cols):
            pt = (x,y)
            if pt in path:
                continue
            # print(f"Checking {pt}")
            is_inside = is_point_in_loop(pt, grid_size, path)
            if is_inside:
                inside.add(pt)

    return inside.difference(path)

EIGHT_VECS = [
    [-1,-1],[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0]
]

def is_pair_open(left, right, axis):
    if axis=='x':
        return left in [VPIPE, LU, LD] and right in [VPIPE, RU, RD]
    elif axis == 'y':
        return left in [HPIPE, RU, LU] and right in [HPIPE, LD, RD]
    
    return False


def flood_fill_from_outside(grid: Grid, border):
    outside = set()
    n_rows = grid.size[0]
    n_cols = grid.size[1]
    corners = [
        (0,0),         (0,n_rows-1), 
        (n_cols-1, 0), (n_cols-1, n_rows-1)
    ]
    queue = Queue()

    for cx,cy in corners:
        if (cx,cy) in border:
            print(f"Skipping {(cx,cy)} in border")
            continue
        queue.put((cx,cy,True))

    seen = set()
    while not queue.empty():
        x,y,is_exact = queue.get()
        exact_nbs = []

        if (x,y) in border:
            continue

        if is_exact:
            outside.add((x,y))
            seen.add((x,y))

            ## Check the exact neighbours
            for v in EIGHT_VECS:
                nx,ny = (x+v[0],y+v[1])
                if nx >= 0 and ny >= 0 and nx < n_cols and ny < n_rows:
                    exact_nbs.append((nx,ny))

        else:
            ## Virtual cell
            xs = [int(x)-1,int(x),int(x)+1]
            ys = [int(y)-1,int(y),int(y)+1]

            if x != int(x):
                ## Virtual along x-axis
                x1 = int(np.floor(x))
                x2 = x1+1
                xs = [x1,x2]
            if y != int(y):
                ## Virtual along y-axis
                y1 = int(np.floor(y))
                y2 = y1+1
                ys = [y1,y2]

            ## Find the (up to 6) real neighbours around this virtual cell
            ## Scroll right
            for nx in xs:
                if nx >= 0 and ny >= 0 and nx < n_cols and ny < n_rows:
                    exact_nbs.append((nx,ys[0]))
            ## Scroll down
            for ny in ys[1:]:
                if nx >= 0 and ny >= 0 and nx < n_cols and ny < n_rows:
                    exact_nbs.append((xs[-1],ny))
            ## Scroll left
            for nx in reversed(xs[:-1]):
                if nx >= 0 and ny >= 0 and nx < n_cols and ny < n_rows:
                    exact_nbs.append((nx,ys[-1]))
            ## Scroll up
            for ny in reversed(ys[:-1]):
                if nx >= 0 and ny >= 0 and nx < n_cols and ny < n_rows:
                    exact_nbs.append((xs[0],ny))

        ## Now check for virtual neighbours, between the adjacent exact neighbours
        # if verbose:
        #     grid2 = copy_grid(grid)
        #     grid2.set(int(x),int(y),'X')
        #     for i,nb in enumerate(exact_nbs):
        #         grid2.set(int(nb[0]), int(nb[1]), str(i))
        #     grid2.show()

        for i,nb in enumerate(exact_nbs):
            nx,ny = nb
            if (nx,ny) in seen:
                continue
            if (nx,ny) not in border:# and (x,y) not in border:
                queue.put((nx,ny,True))
                seen.add((nx,ny))
            else:
                ## Check the virtual neighbour between this and the next exact neighbour
                next_nb = exact_nbs[(i+1)%len(exact_nbs)]
                nnx, nny = next_nb
                nb1 = grid.get(nx,ny)
                nb2 = grid.get(nnx, nny)
                ## Are we comparing symbols in the same row or the same column?
                axis = 'y' if nx == nnx else 'x'
                flip_round = (axis == 'x' and nx > nnx) or (axis == 'y' and ny > nny)
                ## Make sure we consider the symbols from left-to-right
                if flip_round:
                    virtual_enterable = is_pair_open(nb2, nb1, axis)
                else:
                    virtual_enterable = is_pair_open(nb1, nb2, axis)

                virtual_nb = (nx+nnx)/2, (ny+nny)/2

                if virtual_enterable and not virtual_nb in seen:
                    queue.put((virtual_nb[0], virtual_nb[1], False))
                    seen.add(virtual_nb)



    grid = Grid(n_rows, n_cols, 'I')
    for x,y in outside:
        grid.set(x,y,'.')
    for x,y in border:
        grid.set(x,y,'#')
    grid.save('output-grid.txt')
    print()
    return outside

def part_two(fileaddr):
    grid = read_file(fileaddr)
    start_pos = grid.start_pos
    print("Start:", start_pos)
    dist_map = run_dfs_on_path(grid, start_pos)
    unordered_path = list(dist_map.keys())

    path = [unordered_path[0]] 
    ## Add the "right" side of the path
    path.extend(unordered_path[1::2])
    ## Add the left side of the path (reversed so it's from the end of the right side to the beginning)
    path.extend(reversed(unordered_path[2::2]))
    # print(path)

    grid.set_border(path)
    grid.show_border()
    grid.save('output-border.txt', border_only=True)

    grid_size = grid.size
    print("Grid-size:",grid_size)

    outside = flood_fill_from_outside(grid, path)
    n_cells = grid_size[0] * grid_size[1]
    n_inside = n_cells - len(outside) - len(path) 
    # inside = find_inside_outside_2(path, grid_size)
    # n_inside = len(inside)
    # print("Inside:", inside)

    return n_inside









if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if part == '1':
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
