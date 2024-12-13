import numpy as np




def load_file(fname):
    with open(fname, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    return lines


def print_grid(grid):
    for row in grid:
        print(row)

def print_area(area, grid):
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        line = ""
        for x in range(cols):
            if (x,y) in area:
                line += grid[y][x]
            else:
                line += "."
        print(line)


def neighbours(x, y, rows, cols):
    nbs = []
    if x < cols-1:
        nbs.append((x+1,y))
    if x > 0:
        nbs.append((x-1,y))
    if y < rows-1:
        nbs.append((x,y+1))
    if y > 0:
        nbs.append((x,y-1))
    return nbs



def find_areas(grid):
    rows = len(grid)
    cols = len(grid[0])

    visited = np.zeros([rows,cols])

    areas = []

    for y in range(rows):
        for x in range(cols):
            if visited[y][x] > 0:
                continue

            ## Start BFS from this cell
            queue = [(x,y)]

            visited[y][x] = 1
            symbol = grid[y][x]
            area = []

            while len(queue) > 0:
                x,y = queue[0]
                queue = queue[1:]
                area.append((x,y))

                for nx,ny in neighbours(x, y, rows, cols):
                    if grid[ny][nx] == symbol and visited[ny][nx] == 0:
                        visited[ny][nx] = 1
                        queue.append((nx,ny))
            
            areas.append(area)

    return areas


def area_to_outline(area, grid):
    rows = len(grid)
    cols = len(grid[0])

    outline = []

    x,y = area[0]
    symbol = grid[y][x]

    area_units = len(area)
    perimeter = 0

    for pt in area:
        nbs = neighbours(pt[0], pt[1], rows, cols)

        # Count the num of neighbours which are outside this plot.
        # We also include any neighbours outside the grid.
        n_not_same = sum([1 for (nx,ny) in nbs if grid[ny][nx] != symbol]) + 4 - len(nbs)

        ## Only keep points which touch at least one cell outside the plot
        if n_not_same > 0:
            outline.append(pt)

        perimeter += n_not_same

    return outline, perimeter, area_units



def calc_cost(areas, grid, print_areas=False):
    total_cost = 0

    print("Areas:")
    for area in areas:
        outline, perimeter, area_units = area_to_outline(area, grid)
        x,y = area[0]
        sym = grid[y][x]
        # print(f"Symbol={sym}")
        # print(f"Area={area}")
        # print(f"Outline={outline}")
        cost = perimeter * area_units
        # print(f"Perimeter={perimeter}; Area={area_units}")
        # print(f"Cost={cost}")
        # print("-"*30)

        print(f" - {sym} plants with price {perimeter} * {area_units} = {cost}")

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

    total_cost = calc_cost(areas, grid, show_areas)
    print("Total Cost:", total_cost)