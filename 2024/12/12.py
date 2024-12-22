import numpy as np




def load_file(fname):
    with open(fname, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    return lines


def print_grid(grid):
    for row in grid:
        print(row)





def print_area(area, grid, blank='.'):
    """ Print this area to the console only, replacing all other cells in the grid with the blank string. """
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        line = ""
        for x in range(cols):
            if (x,y) in area:
                line += grid[y][x]
            else:
                line += blank
        print(line)


def neighbours(x, y, rows, cols, type=4):
    """
        Get a list of valid neighbours for this cell. Valid means the neighbour falls within the grid coordinates.
        By default, returns the 4-neighbourhood (only the cardinal directions NORTH, EAST, SOUTH, WEST), but you can pass `type=8` to get the 8-neighbourhood (which includes the diagonals NORTH-EAST, NORTH-WEST, SOUTH-WEST, SOUTH-EAST).
    
    """
    nbs = []
    if x < cols-1:
        nbs.append((x+1,y))
    if x > 0:
        nbs.append((x-1,y))
    if y < rows-1:
        nbs.append((x,y+1))
    if y > 0:
        nbs.append((x,y-1))
    
    if type == 8:
        for vec in [[1,1],[1,-1],[-1,1],[-1,-1]]:
            nx,ny = x+vec[0], y+vec[1]
            if nx >= 0 and ny >= 0 and nx < cols and ny < rows:
                nbs.append((nx,ny))

    return nbs



def count_corners(x,y,grid):
    """
        Count the number of corners (both concave and convex) for the cell (x,y) in the given grid.
        Each cell has up to 4 corners, which are uniquely identified by the two edges which they border.
        For example, the NORTH-EAST corner borders the NORTH and EAST cells.
        Corners are identified by checking which sides continue the plot and also by checking if the diagonal cells are contained within the plot.
        Returns the number of corners.
    """

    ## Clockwise edges (EAST, SOUTH, WEST, NORTH)
    # These can be re-ordered but
    nbs = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

    ## vecs[i] = x-y vector to the corner cell touching nbs[i-1] and nbs[i]
    vecs = [(1,-1),(1,1),(-1,1),(-1,-1)]

    rows = len(grid)
    cols = len(grid[0])

    ## Make a binary mask which is 1 if the plot continues on that side and 0 if it is a different plot.
    ## e.g. [1,0,0,1] indicates that the cell to the East and the cell to the North are part of this plot, while the other two are not.
    mask = []
    for i,nb in enumerate(nbs):
        nx,ny = nb
        cvec = vecs[i]
        if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
            mask.append(0)
        elif grid[ny][nx] == grid[y][x]:
            mask.append(1)
        else:
            ## Concave corner
            mask.append(0)

    # print(f"({x},{y}) has edge mask {mask}")

    n_corners = 0

    ## Use the mask and the diagonal neighbours to determine the number of corners.
    for i in range(4):
        ## Get the index of the previous edge (with wrap-around)
        ## e.g. if i=0, then j=3; if i=2, then j=1.
        j = (i+3)%4

        if mask[j] + mask[i] == 0:
            ## If we have two adjacent sides that do not continue the plot, then we have a convex corner.
            n_corners += 1
        elif mask[j] + mask[i] == 2:
            ## If we have two adjacent sides within the plot, then we have to check for a concave corner.
            cvec = vecs[i]
            dx,dy = x+cvec[0], y+cvec[1]

            ## Diagonal is out-of-bounds, this counts as a corner
            if dx < 0 or dy < 0 or dx >= cols or dy >= rows:
                n_corners += 1
            ## Diagonal is within the plot -> no corner
            elif grid[dy][dx] == grid[y][x]:
                n_corners += 0
            ## Otherwise, diagonal is outside the plot, so we have a concave corner
            else:
                n_corners += 1

    return n_corners



def find_areas(grid):
    """
        Applies Breadth-First-Search to identify all connected-components (plots) within the grid.
        Returns a list, which describes each area via an unordered list of its coordinates.
    """
    rows = len(grid)
    cols = len(grid[0])

    visited = np.zeros([rows,cols], dtype='int')

    areas = []

    for y in range(rows):
        for x in range(cols):
            if visited[y][x] == 0:
                ## Start BFS from this cell
                queue = [(x,y)]

                visited[y][x] = 1
                symbol = grid[y][x]
                area = []

                while len(queue) > 0:
                    cx,cy = queue[0]
                    queue = queue[1:]
                    area.append((cx,cy))

                    for nx,ny in neighbours(cx, cy, rows, cols):
                        if grid[ny][nx] == symbol and visited[ny][nx] == 0:
                            visited[ny][nx] = 1
                            queue.append((nx,ny))
                
                areas.append(area)

    return areas


def area_to_outline(area, grid):
    """
        Converts a connected component in the given grid to an outline by removing all internal cells.
        An internal cell is one which has a minimum distance of 2 to any cell outside the plot.
        In other words, the outline is the set of cells which defines the border of this plot (but this includes any points at concave corners). 
        Returns a list of x-y coordinates which give the minimal outline of the given component.
    """
    rows = len(grid)
    cols = len(grid[0])

    outline = []

    x,y = area[0]
    symbol = grid[y][x]

    area_units = len(area)
    perimeter = 0

    for pt in area:
        nbs = neighbours(pt[0], pt[1], rows, cols, type=8)

        # Count the num of neighbours which are outside this plot.
        # We also include any neighbours outside the grid.
        n_outside = 8 - len(nbs)
        n_diff_nbs = sum([1 for (nx,ny) in nbs if grid[ny][nx] != symbol]) + n_outside

        ## Only keep points which touch at least one cell outside this plot
        if n_diff_nbs > 0:
            outline.append(pt)

        perimeter += n_diff_nbs

    return outline, perimeter, area_units



def count_sides(area, grid):
    """
        Count the number of sides of the given plot's area in the grid.
        For all intents and purposes, area is assumed to be the outline of the area, i.e. does not contain cells that have a minimum distance of 2 to a non-plot cell.  
    """

    ## Rule: num of corners == num of sides
    num_sides = 0

    for pt in area:
        corners = count_corners(pt[0], pt[1], grid)
        # print(f"{pt} has {corners} corners")
        num_sides += corners

    return num_sides





def calc_cost(areas, grid, print_areas=False, part=1):

    """
        Calculates the cost of fencing the areas in the given grid.
        If `print_areas` is true, then the grid will be printed after each area is calculated, showing all excluded cells as '.'.
        Parameter `part` indicates which part of the question is used for calculating cost; if 1, then cost=perimeter*area; if 2, then cost=sides*area.
    
    """

    total_cost = 0

    print("Areas:")
    for area in areas:
        outline, perimeter, area_units = area_to_outline(area, grid)
        x,y = area[0]
        sym = grid[y][x]
        
        if part == 1:
            cost = perimeter * area_units
            print(f" - {sym} plants with price {perimeter} * {area_units} = {cost}")
        else:
            sides = count_sides(outline, grid)
            cost = sides * area_units
            print(f" - {sym} plants with price {sides} * {area_units} = {cost}")

        if print_areas:
            print_area(area, grid)

        total_cost += cost
    
    return total_cost





from sys import argv
from os.path import exists


if __name__ == '__main__':

    if len(argv) < 2:
        print("Missing filename target!")
        exit(1)

    fname = argv[1]

    if not exists(fname):
        print(f"File not found: {fname}")
        exit(1)

    show_areas = False
    if len(argv) > 2 and argv[2] == 'show':
        show_areas = True

    grid = load_file(fname)
    print_grid(grid)

    areas = find_areas(grid)

    total_cost_p1 = calc_cost(areas, grid, show_areas)
    print("(Part 1) Total Cost (perimeter):", total_cost_p1)

    print()
    total_cost_p2 = calc_cost(areas, grid, show_areas, part=2)
    print("(Part 2) Total Cost (sides):", total_cost_p2)