
import numpy as np
from collections import defaultdict
from time import sleep

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
INSIDE = 8
OUTSIDE = 9


def find_border_pts(coords):
    border = list()
    for i,pt1 in enumerate(coords):
        x1,y1 = pt1
        border.append(tuple(pt1))
        pt2 = coords[(i+1) % len(coords)]
        x2,y2 = pt2

        ## Fill in between
        # print(f"Fill {x1},{y1} -> {x2},{y2}")
        if x1 == x2:
            border.extend([(x1,y) for y in range(min(y1,y2)+1,max(y1,y2))])
        if y1 == y2:
            border.extend([(x,y1) for x in range(min(x1,x2)+1,max(x1,x2))])
            
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

code_to_sym = {
    ENCLOSED: '@',
    CORNER: 'X',
    RED: '@',
    GREEN: '*',
    OUTSIDE: 'O',
    INSIDE: 'I'
}


def display_grid(grid):
    n_rows = grid.shape[0]

    for y in range(n_rows):
        line = "".join([code_to_sym.get(char, '.') for char in grid[y]])
        print(line)


def find_largest_rectangle(coords):
    max_area = 0
    chosen = (0,1)
    for i,pt1 in enumerate(coords):
        for j,pt2 in enumerate(coords[i+1:]):
            sorted_pts = sorted([pt1,pt2])
            x1,y1 = sorted_pts[0]
            x2,y2 = sorted_pts[1]
            area = (1+x2-x1)*(1+y2-y1)
            if area > max_area:
                max_area = area
                chosen = (i,i+1+j)

    print(coords[chosen[0]], coords[chosen[1]])
    if len(coords) < 100:
        grid = construct_grid(coords)
        x1,y1 = coords[chosen[0]]
        x2,y2 = coords[chosen[1]]
        grid[y1,x1] = CORNER
        grid[y2,x2] = CORNER
        display_grid(grid)
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
    """
    Applies coordinate compression, removing any points which are on a straight line between two other points.
    """
    start = coords[0]
    simple_pts = [start]
    prev_dir = find_direction(start, coords[1])
    curr = coords[1]

    for i in range(1, len(coords)):
        curr = coords[i]
        prev = coords[i-1]
        direction = find_direction(prev, curr)
        if direction != prev_dir:
            # print(f"{prev} -> {curr}, d={direction}")
            simple_pts.append(prev)
            prev_dir = direction

    ## Always include the last point
    simple_pts.append(coords[-1])

    return simple_pts
    

dirs = [[0,-1],[1,0],[0,1],[-1,0]]

known_outside = set()
known_inside = set()

def is_outside(pt, coords_lookup_by_row, coords_lookup_by_col, verbose=False):
    if pt in known_outside:
        return True
    elif pt in known_inside:
        return False
    
    x,y = pt
    if x in coords_lookup_by_row[y]:
        ## If this point is in the border
        return False
    
    ## Store if we saw a wall in each of the four cardinal directions
    walls_seen = [0,0,0,0]

    row_keys = list(coords_lookup_by_row.keys())

    for d in [UP, DOWN]:
        for yr in row_keys:
            if d == UP and yr >= y:
                break
            elif d == DOWN and yr <= y:
                continue 
            
            ## Scan right looking for if there's a wall that crosses in front of the point
            coords_in_row = sorted(coords_lookup_by_row[yr].keys())
            for i in range(1, len(coords_in_row)):
                x1,x2 = coords_in_row[i-1], coords_in_row[i]
                if x1 <= x and x <= x2:
                    walls_seen[d] = 1
                    break
            if walls_seen[d] > 0:
                break

    col_keys = list(coords_lookup_by_col.keys())

    for d in [LEFT, RIGHT]:
        for col in col_keys:
            if d == LEFT and col >= x:
                continue
            elif d == RIGHT and col <= x:
                continue

            ## Scan down looking for if there's a wall that crosses in front of the point
            coords_in_col = sorted(coords_lookup_by_col[col].keys())
            for i in range(1, len(coords_in_col)):
                y1 = coords_in_col[i-1]
                y2 = coords_in_col[i]
                # if verbose:
                #     print(f"Checking {d} for y={y1}-{y2}")
                if y1 <= y and y <= y2:
                    walls_seen[d] = 1
                    # if verbose:
                    #     print("Wall seen", d)
                    break
            if walls_seen[d] > 0:
                break

    # if verbose:
    #     print(walls_seen)

    ## This point is only inside if all four directions face a wall
    outside = sum(walls_seen) < 4
    # print(walls_seen)
    if outside:
        known_outside.add(pt)
    else:
        known_inside.add(pt)

    return outside





def find_largest_rectangle_excluding(target_pts, box_to_exclude):
    ## Index coords by column for faster lookup
    coords_lookup_by_row = defaultdict(dict)
    coords_lookup_by_col = defaultdict(dict)
    for i,(x,y) in enumerate(target_pts):
        coords_lookup_by_row[y][x] = i
        coords_lookup_by_col[x][y] = i

    border = find_border_pts(target_pts)

    best_rects = []
    max_area = 0
    row_nums = np.array(list(coords_lookup_by_row.keys()))

    pairs_to_check = []

    exclude_box = len(box_to_exclude) > 0
    excl_width = 0

    if exclude_box:
        excluded_mins = np.min(box_to_exclude, axis=0)
        excluded_maxs = np.max(box_to_exclude, axis=0)
        excl_x1, excl_y1 = excluded_mins[0], excluded_mins[1]
        excl_x2, excl_y2 = excluded_maxs[0], excluded_maxs[1]
        excl_width = excl_x2 - excl_x1
        print(f"Excluded: x={excl_x1}-{excl_x2}, y={excl_y1}-{excl_y2}")

    for p1i,(x1,y1) in enumerate(target_pts):
        selected_row_nums = row_nums[np.argwhere(row_nums > y1).flatten()]
        ## Check all points below this one
        for y2 in selected_row_nums:
            if exclude_box:
                if (y1 < excl_y1 and y2 > excl_y1) or (y1 < excl_y2 and y2 >= excl_y2):
                    break
            coords_on_row = coords_lookup_by_row[y2]
            ## Check all points to the right
            for x2 in list(coords_on_row.keys()):
                if x2 < x1 + excl_width // 2:
                    continue
                p2i = coords_on_row[x2]
                pairs_to_check.append((p1i,p2i))

    def estimate_area(point_idx):
        p1 = target_pts[point_idx[0]]
        p2 = target_pts[point_idx[1]]
        return (1+abs(p1[0]-p2[0])) * (1+abs(p1[1]-p2[1]))
    
    ## Sort the regions from largest to smallest
    ## So we find the largest area first and then disregard the rest
    pairs_to_check = sorted(pairs_to_check, key=estimate_area, reverse=True)
    print(f"Found {len(pairs_to_check)} pairs!")
    print_step = min(100, len(pairs_to_check) / 4)

    ## ([4069, 63210], [96497, 64308])
    ## 4, 63, 96, 64

    for i,(p1i,p2i) in enumerate(pairs_to_check):
        x1,y1 = target_pts[p1i]
        x2,y2 = target_pts[p2i]

        if (i+1) % print_step == 0:
            overall_progress = i / len(pairs_to_check)
            print(f"Pair {i+1} ({overall_progress:0.1%}):", target_pts[p1i], target_pts[p2i], end='\r')

        area = estimate_area([p1i, p2i])

        ## Early exit if this rectangle isn't a new best
        if area <= max_area:
            continue

        is_valid = True

        if len(box_to_exclude) > 0:
            overlap_left = x1 <= excl_x1 and excl_x1 < x2
            overlap_right = x1 < excl_x2 and excl_x2 <= x2
            overlap_top = y1 <= excl_y1 and excl_y1 < y2
            overlap_bottom = y1 < excl_y2 and excl_y2 <= y2
            overlap_horizontal = excl_x1 <= x1 and x2 <= excl_x2
            overlap_vertical = excl_y1 <= y1 and y2 <= excl_y2
            if (overlap_left or overlap_right or overlap_horizontal) and (overlap_top or overlap_bottom or overlap_vertical):
                is_valid = False
        
        if not is_valid:
            continue

        ## We only need to check if the two other corners are in
        for x,y in [(x1,y2),(x2,y1)]:
            if (x,y) in border:
                continue
            if is_outside((x,y), coords_lookup_by_row, coords_lookup_by_col):
                is_valid = False
                # print(f"{(x,y)} is out!")
                break

        if is_valid:
            print(f"\nNew best with area {area}")
            max_area = max(area, max_area)
            best_rects.append((p1i,p2i))

    print("\nProgress: 100.0%")

    if max_area > 0:
        best_rect = best_rects[-1]
        rect_corners = target_pts[best_rect[0]], target_pts[best_rect[1]]
        ## Expected (for scale=1000): rect_corners = [2,51], [96,60]
        print(rect_corners)
        scale_factor = 1
        max_width = max(np.max(target_pts, axis=1))
        display_width = 400
        if max_width > display_width:
            scale_factor = int(np.ceil(max_width / display_width))
            target_pts = [tuple(np.array(pt) // scale_factor) for pt in target_pts]
        grid = construct_grid_part_2(target_pts)
        x1,y1 = tuple(np.array(rect_corners[0]) // scale_factor)
        x2,y2 = tuple(np.array(rect_corners[1]) // scale_factor)
        for xc in [x1,x2]:
            for yc in [y1,y2]:
                grid[yc,xc] = CORNER
        new_grid = np.zeros((y2+3-y1+3,18))
        print(new_grid.shape)
        new_grid[:,:6] = grid[y1-3:y2+3,x1-3:x1+3]
        new_grid[:,6:12] = BLANK
        new_grid[:,12:] = grid[y1-3:y2+3,x2-3:x2+3]
        display_grid(new_grid)
    else:
        print("No solutions!")

    return max_area


def find_largest_rectangle_part_2_narrow(target_pts, box_to_exclude):
    ## Index coords by column for faster lookup
    coords_lookup_by_row = defaultdict(dict)
    coords_lookup_by_col = defaultdict(dict)
    for i,(x,y) in enumerate(target_pts):
        coords_lookup_by_row[y][x] = i
        coords_lookup_by_col[x][y] = i

    border = set(find_border_pts(target_pts))

    excluded_mins = np.min(box_to_exclude, axis=0)
    excluded_maxs = np.max(box_to_exclude, axis=0)
    excl_x1, excl_y1 = excluded_mins[0], excluded_mins[1]
    excl_x2, excl_y2 = excluded_maxs[0], excluded_maxs[1]
    print(f"Excluded: x={excl_x1}-{excl_x2}, y={excl_y1}-{excl_y2}")

    best_pair = []
    max_area = 0
    y1 = excl_y2
    max_y = np.max(target_pts, axis=0)[1]
    x1 = np.min(list(coords_lookup_by_row[y1].keys()))

    while y1 < max_y:
        coords_on_row = list(coords_lookup_by_row[y1].keys())
        if len(coords_on_row) < 2:
            break
        
        ## Find the widest rectangle with its top on row y1
        x2 = np.max(coords_on_row)
        y2 = y1
        # print(f"Checking {x1},{y1} -> {x2},{y2}")

        ## Now descend until either end point falls outside the shape
        while (x1,y2+1) in border and (x2,y2+1) in border:
            # print(f"Inc y2, {x1},{y1}, {x2},{y2}")
            y2 += 1

        print("Got:", x1,y1,x2,y2)
        area = (1+y2-y1) * (1+x2-x1)
        if area > max_area:
            area = max_area
            print(area)
            best_pair = ((x1,y1),(x2,y2))

        ## Jump to the next point
        y1 = y2

        while (x1,y1+1) in border:
            # print(f"Inc y1, {x1},{y1}, {x2},{y2}")
            y1+=1

        last = DOWN

        while (x1,y1+1) not in border:
            # print(f"Inc x1, {x1},{y1}, {x2},{y2}")
            # print("Next", x1+1, y1)
            move_right = (x1+1,y1) in border
            move_left = (x1-1,y1) in border
            move_down = (x1,y1+1) in border
            if move_down:
                break
            elif move_right:
                last = RIGHT
                x1 += 1
            elif move_left and last != RIGHT:
                last = LEFT
                x1 -= 1
            else:
                break

            # if x1 == 46:
            #     grid = construct_grid_part_2(target_pts)
            #     grid[y1,x1] = CORNER
            #     display_grid(grid[y1-3:y1+3,x1-5:x1+5])
            #     break
    
    scale_factor = 1
    max_width = max(np.max(target_pts, axis=1))
    display_width = 300
    if max_width > display_width:
        scale_factor = int(np.ceil(max_width / display_width))
        target_pts = [tuple(np.array(pt) // scale_factor) for pt in target_pts]
    grid = construct_grid_part_2(target_pts)
    x1,y1 = tuple(np.array(best_pair[0]) // scale_factor)
    x2,y2 = tuple(np.array(best_pair[1]) // scale_factor)
    for xc in [x1,x2]:
        for yc in [y1,y2]:
            grid[yc,xc] = CORNER
    display_grid(grid[y1-3:y2+5,x1-5:x1+5])

    return max_area







def find_indent(coords, width=10):
    """
    Find the coordinates of the corner of a shape with horizontal sides of length 'width'.
    """
    indent_corners = []
    for i in range(1, len(coords)):
        curr = coords[i]
        prev = coords[i-1]
        length = abs(curr[0] - prev[0])
        if length > width:
            indent_corners.extend([prev,curr])

    indent = sorted(indent_corners)
    return indent


from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    coords = load(fname)

    part = '1'
    if len(argv) > 2:
        part = argv[2]

    # if part == '1':
    #     largest_rect_area = find_largest_rectangle(coords)
    #     print("Part 1:", largest_rect_area)

    if part == '2':
        if fname != 'test.txt':
            raise Exception("Part 2 solution is only designed for 'test.txt'!")
        
        scale_factor = 1
        if scale_factor > 1:
            coords = np.array(coords) // scale_factor
            coords = coords.tolist()
        simple_pts = simplify_coords(coords)
        indent_corners = find_indent(simple_pts, 10000//scale_factor)
        print("Indent corners:",indent_corners)

        largest_enclosed_rect_area = find_largest_rectangle_excluding(coords, indent_corners)
        print("Part 2:", largest_enclosed_rect_area)
