
import numpy as np
from collections import defaultdict


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


def find_encoded_border(coords):
    rows = defaultdict(list)
    cols = defaultdict(list)

    for i, curr in enumerate(coords):
        x1,y1 = curr
        x2,y2 = coords[(i+1) % len(coords)]
        min_x, max_x = min(x1,x2), max(x1,x2)
        min_y, max_y = min(y1,y2), max(y1,y2)

        if x1 == x2:
            x = x1
            cols[x].append([min_y,max_y])
            for y in range(min_y,max_y+1):
                rows[y].append([x,x])
                
        else:
            y = y1
            rows[y].append([min_x,max_x])
            for x in range(min_x,max_x+1):
                cols[x].append([y,y])

    rows_flat = {}
    cols_flat = {}

    for y, xs in rows.items():
        xs = sorted(xs)
        # print(y, xs)
        xs_new = []
        rows_flat[y] = xs_new
        if len(xs) == 0:
            continue
        xs_new.append(xs[0])
        for i in range(1, len(xs)):
            a,b = xs[i]
            # print(xs_new[-1], xs[i])
            la,lb = xs_new[-1][0],xs_new[-1][1]
            if a <= lb or la == lb or a == b:
                xs_new[-1][1] = max(lb, b)
            else:
                xs_new.append(xs[i])
        rows_flat[y] = np.array(xs_new)

    for x, ys in cols.items():
        ys = sorted(ys)
        ys_new = []
        cols_flat[x] = ys_new
        if len(ys) == 0:
            continue
        ys_new.append(ys[0])
        for i in range(1, len(ys)):
            a,b = ys[i]
            la,lb = ys_new[-1][0], ys_new[-1][1]
            if a <= lb or la == lb or a == b:
                ys_new[-1][1] = max(lb, b)
            else:
                ys_new.append(ys[i])
        cols_flat[x] = np.array(ys_new)


    return rows_flat, cols_flat



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




# from queue import Queue

# def flood_to_fill_inner(start, border):
#     frontier = Queue()
#     frontier.put(start)

#     maxs = np.max(border, axis=0)
#     max_x = maxs[0]
#     max_y = maxs[1]
#     visited = set()

#     ## BFS to explore until we reach the edge of the grid
#     while not frontier.empty():
#         curr = frontier.get()
#         if curr in visited:
#             continue
#         # print(curr)
#         visited.add(curr)
#         x,y = curr
#         nbs = [(x-1,y),(x,y-1),(x+1,y),(x,y+1)]

#         for nx,ny in nbs:
#             if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
#                 ## Spread outside the known red/green regions
#                 return None
#             elif (nx,ny) not in visited and (nx,ny) not in border:
#                 frontier.put((nx,ny))
            
#     return visited



# def find_enclosed_pts(coords, border):
#     ## Find the line between the first two points
#     (x1,y1) = coords[0]
#     (x2,y2) = coords[1]

#     x1,x2 = min(x1,x2),max(x1,x2)
#     y1,y2 = min(y1,y2),max(y1,y2)

#     x3,y3 = (x1+(x2-x1)//2, y1+(y2-y1)//2)

#     if y1 == y2:
#         ## Horizontal line, check above/below the midpoint
#         area = flood_to_fill_inner((x3,y3-1), border)
#         if area is None:
#             print("Not above")
#             ## Check below the line
#             area = flood_to_fill_inner((x3,y3+1), border)
#     else:
#         ## Vertical line, check left/right of the midpoint
#         area = flood_to_fill_inner((x3-1,y3), border)
#         if area is None:
#             print("Not left")
#             ## Check right of the line
#             area = flood_to_fill_inner((x3+1,y3), border)

#     if not area:
#         return []
    
#     return area

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

def find_direction(first, second):
    if first[0] == second[0]:
        ## X is same
        return DOWN if first[1] < second[1] else UP
    ## Y is same
    return RIGHT if first[0] < second[0] else LEFT
        


def simplify_coords(coords):
    start = coords[0]
    simple_pts = [start]
    prev_dir = find_direction(start, coords[1])
    curr = coords[1]

    for i in range(1, len(coords)):
        curr = coords[i]
        prev = coords[i-1]
        direction = find_direction(prev, curr)
        if direction != prev_dir:
            simple_pts.append(prev)
            prev_dir = direction

    ## Always include the last point
    simple_pts.append(coords[-1])
    return simple_pts
    



def find_largest_enclosed_rectangle(coords):
    border = find_border_pts(coords)
    max_area = 0
    chosen = (0,1)
    total_pairs = len(coords) * (len(coords)-1) / 2

    simple_pts = simplify_coords(coords)
    rows, cols = find_encoded_border(simple_pts)

    ## Index coords by column for faster lookup
    coords_by_col = defaultdict(dict)
    for i,(x,y) in enumerate(coords):
        coords_by_col[y][x] = i

    progress = 0
    for i,(x1,y1) in enumerate(coords):
        ## Check all points to the right and below
        for y2, coords_on_row in coords_by_col.items():
            if y2 <= y1:
                continue

            for x2, j in coords_on_row.items():
                if x2 <= x1:
                    continue

                progress += 1
                # print(progress, "/", total_pairs)

                x1,x2 = min(x1,x2),max(x1,x2)
                y1,y2 = min(y1,y2),max(y1,y2)
                area = (1+x2-x1)*(1+y2-y1)

                ## Early exit if this rectangle isn't a new best
                if area <= max_area:
                    continue

                is_valid = True

                print("Evaluating:", coords[i], coords[j])
                grid = construct_grid_part_2(coords)
                grid[y1,x1] = CORNER
                grid[y1,x2] = CORNER
                grid[y2,x1] = CORNER
                grid[y2,x2] = CORNER
                display_grid(grid)

                ## Check for gaps
                for y in range(y1,y2):
                    row = rows[y]
                    print("Checking row", y, "with", row.tolist(), f"for x={x1}-{x2}")

                    if x1 < row[0,0] or x2 > row[-1,1]:
                        is_valid=False
                        print("Invalid due to edges on row", y)
                        break

                    l = 0
                    while l < row.shape[0]-1 and row[l+1,0] <= x1:
                        l += 1
                    print(f" > l={l}")

                    l2 = l
                    while l2 < row.shape[0] and row[l2,1] < x2:
                        l2 += 1

                    if l2 >= row.shape[0]:
                        is_valid = False
                        break

                    within_shape = row[l,0] <= x1 and row[l2,1] >= x2 and (l2-l) <= 1
                    if within_shape:
                        print(f"Within shape on row {y} for l = {l}")
                        continue

                    non_coords = set(range(x1,x2+1)).difference(coords_by_col[y].keys())
                    if len(non_coords) > 0:
                        print(f"Invalid due to non-coords {non_coords} on row {y}")
                        is_valid = False
                        break

                if not is_valid:
                    continue

                # for x in range(x1,x2+1):
                #     up = np.argwhere(cols[x] > y1).flatten()
                #     print("Checking col", x, "with", cols[x], "for", y1, y2, "->", up)
                #     ## Check if the height of the rectangle is contained in this region
                #     is_valid = len(up) > 0 and up[0] % 2 == 1 and cols[x][up[0]] >= y2
                #     if not is_valid:
                #         print(f"Invalid due to {up} on col {x}")
                #         break

                if is_valid:
                    print("New best:", (i,i+1+j), f"with area {area}")
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

    # largest_enclosed_rect_area = find_largest_enclosed_rectangle(coords)
    # print("Part 2:", largest_enclosed_rect_area)

    r,c = find_encoded_border(coords)
    print(r)
    # print(c)

    grid = construct_grid_part_2(coords)
    display_grid(grid)