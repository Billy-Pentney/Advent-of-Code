
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        coords = [
            tuple([int(x) for x in row.strip("\n").split(",")])
            for row in file.readlines()
        ]

    return coords

def construct_grid(coords):
    max_vals = np.max(coords, axis=0)
    grid = np.zeros((max_vals[1]+2, max_vals[0]+2))
    for (x,y) in coords:
        grid[y,x] = RED
    return grid

BLANK = 0
RED = 1
GREEN = 2
ENCLOSED = 4
CORNER = 5

def find_border_pts(coords):
    border = []
    for i,pt1 in enumerate(coords):
        x1,y1 = pt1
        border.append(pt1)
        pt2 = coords[(i+1) % len(coords)]
        x2,y2 = pt2

        ## Fill in between
        if x1 == x2:
            for y in range(min(y1,y2)+1,max(y1,y2)):
                border.append((x1,y))
        elif y1 == y2:
            for x in range(min(x1,x2)+1,max(x1,x2)):
                border.append((x,y1))
        
        border.append(pt2)
    
    return border


def construct_grid_part_2(coords):
    max_vals = np.max(coords, axis=0)
    grid = np.zeros((max_vals[1]+2, max_vals[0]+2))
    border = find_border_pts(coords)

    for pt in border:
        grid[pt[1],pt[0]] = GREEN

    for pt in coords:
        grid[pt[1],pt[0]] = RED

    return grid


def display_grid(grid):
    n_rows = grid.shape[0]
    n_cols = grid.shape[1]

    for y in range(n_rows):
        line = ""
        for x in range(n_cols):
            if grid[y,x] == ENCLOSED:
                line += '@'
            elif grid[y,x] == CORNER:
                line += "X"
            elif grid[y,x] == RED:
                line += "R"
            elif grid[y,x] == GREEN:
                line += "G"
            else:
                line += "."

        print(line)



## Unit vectors in North, East, South, West
vecs = [[0,-1],[1,0],[0,1],[-1,0]]
enclosed_cache = {}

def is_point_enclosed(pt, border):
    
    if pt in enclosed_cache.keys():
        return enclosed_cache[pt]
    
    if pt in border:
        enclosed_cache[pt] = True
        return True
    
    maxs = np.max(border, axis=0)
    max_x = maxs[0]
    max_y = maxs[1]

    ## Count the number of times we cross a border, once in each cardinal direction
    seen_border = 0
    
    for i,vec in enumerate(vecs):
        x,y = pt
        # print(f"Direction {i}")

        ## Keep stepping until we reach the edge
        while x >= 0 and x < max_x and y >= 0 and y < max_y:
            print(x,y)
            x += vec[0]
            y += vec[1]
            ## If we cross the border
            if (x,y) in border:
                seen_border += 1
                break

    is_enclosed = seen_border == 4
    # if is_enclosed:
    #     print(f"Point {pt} is enclosed")

    enclosed_cache[pt] = is_enclosed
    return is_enclosed


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


def find_rectangle_border(pt1, pt2):
    x1,x2 = min(pt2[0],pt1[0]),max(pt2[0],pt1[0])
    y1,y2 = min(pt2[1],pt1[1]),max(pt2[1],pt1[1])
    border = []
    border.append((x1,y1))
    x,y = x1,y1
    while x < x2:
        border.append((x,y))
        x += 1
    while y < y2:
        border.append((x,y))
        y += 1
    while x > x1:
        border.append((x,y))
        x -= 1
    while y > y1:
        border.append((x,y))
        y -= 1
    return border

def find_rectangle_points(pt1, pt2):
    x1,x2 = min(pt2[0],pt1[0]),max(pt2[0],pt1[0])
    y1,y2 = min(pt2[1],pt1[1]),max(pt2[1],pt1[1])
    all_pts = [
        (x,y)
        for x in range(x1,x2)
        for y in range(y1,y2)
    ]
    return all_pts




from queue import Queue

def flood_to_fill_inner(start, border):
    frontier = Queue()
    frontier.put(start)

    maxs = np.max(border, axis=0)
    max_x = maxs[0]
    max_y = maxs[1]
    visited = set()

    ## BFS to explore until we reach the edge of the grid
    while not frontier.empty():
        curr = frontier.get()
        if curr in visited:
            continue
        # print(curr)
        visited.add(curr)
        x,y = curr
        nbs = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

        for nx,ny in nbs:
            if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                ## Spread outside the known red/green regions
                return None
            elif (nx,ny) not in visited and (nx,ny) not in border:
                frontier.put((nx,ny))
            
    return visited



def find_enclosed_pts(coords, border):
    ## Find the line between the first two points
    (x1,y1) = coords[0]
    (x2,y2) = coords[1]

    x1,x2 = min(x1,x2),max(x1,x2)
    y1,y2 = min(y1,y2),max(y1,y2)

    x3,y3 = (x1+(x2-x1)//2, y1+(y2-y1)//2)

    if y1 == y2:
        ## Horizontal line, check above/below the midpoint
        area = flood_to_fill_inner((x3,y3-1), border)
        if area is None:
            print("Not above")
            ## Check below the line
            area = flood_to_fill_inner((x3,y3+1), border)
    else:
        ## Vertical line, check left/right of the midpoint
        area = flood_to_fill_inner((x3-1,y3), border)
        if area is None:
            print("Not left")
            ## Check right of the line
            area = flood_to_fill_inner((x3+1,y3), border)

    if not area:
        return []
    
    return area




def find_largest_enclosed_rectangle(coords):
    border = find_border_pts(coords)
    max_area = 0
    chosen = (0,1)
    total_pairs = len(coords) * (len(coords)-1) / 2

    border = find_border_pts(coords)
    print(border)
    enclosed_area = find_enclosed_pts(coords, border)
    print(enclosed_area)

    progress = 0
    for i,pt1 in enumerate(coords):
        for j,pt2 in enumerate(coords[i+1:]):
            progress += 1
            # print(progress, "/", total_pairs)

            x1,x2 = min(pt2[0],pt1[0]),max(pt2[0],pt1[0])
            y1,y2 = min(pt2[1],pt1[1]),max(pt2[1],pt1[1])
            area = (1+x2-x1)*(1+y2-y1)
            if area <= max_area:
                continue

            rect_points = find_rectangle_points((x1,y1), (x2,y2))
            rect_border = find_rectangle_border((x1,y1), (x2,y2))
            ## Find all points in the rectangle that aren't in the red/green region
            rect_points = set(rect_points).difference(rect_border)
            rect_not_enclosed = set(rect_points).difference(enclosed_area) 

            if len(rect_not_enclosed) == 0:
                print("New best: ", (i,i+1+j), f" with area {area}")
                max_area = area
                chosen = (i,i+1+j)

    print(coords[chosen[0]], coords[chosen[1]])
    grid = construct_grid_part_2(coords)
    x1,y1 = coords[chosen[0]]
    x2,y2 = coords[chosen[1]]
    grid[y1,x1] = CORNER
    grid[y1,x2] = CORNER
    grid[y2,x1] = CORNER
    grid[y2,x2] = CORNER
    display_grid(grid)
    return max_area







from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    coords = load(fname)

    # largest_rect_area = find_largest_rectangle(coords)
    # print("Part 1:", largest_rect_area)

    # grid = construct_grid_part_2(coords)

    # border = find_border_pts(coords)
    # for y in range(grid.shape[0]):
    #     for x in range(grid.shape[1]):
    #         if is_point_enclosed((x,y), border):
    #             grid[y,x] = ENCLOSED

    # display_grid(grid)

    largest_enclosed_rect_area = find_largest_enclosed_rectangle(coords)
    print("Part 2:", largest_enclosed_rect_area)