
import numpy as np
import regex as re
from collections import namedtuple
from time import sleep 

Region = namedtuple("Region", ["width", "length", "reqs"])
sleep_delay_secs = 0


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    presents = []
    regions = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if len(lines[i].strip()) == 0:
            i+=1
            continue
        match_present = re.match("(\d+):", line)
        if match_present:
            present_num = int(match_present.group(1))
            present = []
            while i < len(lines)-1 and len(lines[i+1]) > 0:
                i += 1
                present.append(list(lines[i]))
            ## Binarize the present (0 = free, 1 = occupied)
            presents.append(np.where(np.array(present) == '#', 1, 0))
            continue

        match_region = re.match("(\d+)x(\d+):((?: \d+)+)", line)
        if match_region:
            w = int(match_region.group(1))
            h = int(match_region.group(2))
            reqs = [int(num) for num in match_region.group(3).strip().split(" ")]
            regions.append(Region(w,h,reqs))

        i+=1

    return presents, regions

def print_grid(grid):
    print("")
    for x in range(grid.shape[1]):
        line = []
        for y in range(grid.shape[0]):
            if grid[y,x] < 1:
                line.append(".")
            elif grid[y,x] == 1:
                line.append('#')
            else:
                line.append('X')
        print("".join(line))


def rotate_shape(present):
    """Performs a single 90 degree rotation of the given array."""
    return np.rot90(present)
                 

def check_for_too_many_presents(grid, presents):
    present_areas = [np.count_nonzero(present) for present in presents]
    total_present_areas = sum(present_areas)
    grid_area = grid.size
    print("Total Presents:", total_present_areas)
    print("Total Grid:", grid_area)
    return total_present_areas > grid_area
        
shape_rotations = {}


def try_placement(grid, presents):
    """
    Attempts to recursively place the remaining presents.
    Returns the grid after a successful placement of all remaining presents.
    
    :param grid: A 2D binary array in which the presents are to be placed.
    :param presents: A list of 2D binary arrays, indicating the shape of each present.
    :param i: The index of the first present yet to be placed.
    """
    if len(presents) == 0:
        print_grid(grid)
        return grid
        
    valid_moves = []

    ## Check each present
    present_i = 0
    present_idx = presents[present_i]
    # for present_i, present_idx in enumerate(presents):
    present_rots = shape_rotations[present_idx]

    ## Check each 90 degree rotation
    for r,rot_shape in enumerate(present_rots):
        present_width, present_height = rot_shape.shape[0], rot_shape.shape[1]

        ## The range of values where we can place the top-left of the present
        min_x, min_y = 0, 0
        max_x, max_y = grid.shape[0]-present_width, grid.shape[1]-present_height

        ## Find the set of points which are filled in the shape
        present_points = [(x,y) for (x,y) in np.argwhere(rot_shape == 1)]

        ## Find the set of points that border the filled present shape
        perimeter = set([
            (xp+dx,yp+dy)
            for xp,yp in present_points
            ## Consider the 3x3 area around each point in a shape
            for dx in range(-1,2)
            for dy in range(-1,2)
            if dx != dy or dx != 0
        ])
        ## Remove any points already in the shape
        perimeter = list(perimeter.difference(present_points))

        for x in range(min_x, max_x+1):
            x2 = x + present_width
            for y in range(min_y, max_y+1):
                y2 = y + present_height

                grid2 = grid.copy()
                ## Binary operation to mark the occupied cells
                grid2[x:x2,y:y2] = grid2[x:x2,y:y2] + rot_shape

                ## Count the number of cells with more than one shape
                if np.count_nonzero(grid2 > 1) > 0:
                    continue

                ## Calculate the cost of this placement by checking how many exposed cells it leaves
                ## Find the list of points which border this shape
                ## Select the perimeter cells in the grid bounds
                this_perimeter = [
                    (x+a,y+b) for (a,b) in perimeter
                    if x+a >= 0 and x+a < grid2.shape[0] and y+b >= 0 and y+b < grid2.shape[1]
                ]

                ## Calculate a cost for this placement, based on how many cells border a blank cell.
                ## This encourages the algorithm to fill gaps!
                cost = 0
                ## Select all points that are blank after placement.
                empty_perimeter = [(nx,ny) for (nx,ny) in this_perimeter if grid2[nx,ny] == 0]
                ## Now count all points in the present which have at least one blank neighbour
                for xp,yp in present_points:
                    for v in [(-1,0),(1,0),(0,1),(0,-1)]:
                        nb = (xp+x+v[0],yp+y+v[1])
                        if nb in empty_perimeter:
                            cost += 1
                            break
                
                valid_moves.append((present_i, r, x, y, cost))
       
    ## No valid moves were found
    if len(valid_moves) == 0:
        return None
    
    ## Sort by increasing cost
    sorted_moves = sorted(valid_moves, key=lambda it: it[4])

    ## Try each move, recursing until we find a solution
    for (present_i, r, x, y, cost) in sorted_moves:
        present_idx = presents[present_i]
        rot_shape = shape_rotations[present_idx][r]

        ## Recompute the grid after placement
        x2, y2 = x+rot_shape.shape[0], y+rot_shape.shape[1]
        grid2 = np.copy(grid)
        grid2[x:x2,y:y2] = grid2[x:x2,y:y2] + rot_shape

        print_grid(grid2)
        sleep(sleep_delay_secs)

        ## Drop this present, since we used it
        presents2 = presents[:present_i] + presents[present_i+1:]
        grid2 = try_placement(grid2, presents2)

        if grid2 is not None:
            return grid2

    return None



def check_region_suitability(region, presents):
    grid = np.zeros((region.length, region.width))

    present_idxs = []
    for i, num_required in enumerate(region.reqs):
        present_idxs.extend([i] * num_required)

    if check_for_too_many_presents(grid, presents):
        return False

    output_grid = try_placement(grid, present_idxs)
    successful_placement = output_grid is not None
    if successful_placement:
        print_grid(output_grid)

    return successful_placement
            

def count_num_regions_completable(regions, presents):
    num_success = 0
    for r,region in enumerate(regions):
        print(f" --- Region {r+1}")
        shape_rotations.clear()

        ## Pre-compute the four rotations of each present
        for i,present in enumerate(presents):
            shape_rotations[i] = []
            for r in range(3):
                duplicate = False
                ## Check and ignore duplicate rotations
                for j in range(len(shape_rotations[i])):
                    if np.max(shape_rotations[i][j] - present) == 0:
                        duplicate = True
                        break
                if not duplicate:
                    shape_rotations[i].append(present)
                present = rotate_shape(present)

        success = check_region_suitability(region, presents)
        print(f" > Can place? {success}")
        if success:
            num_success += 1

    return num_success


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    if len(argv) > 2:
        sleep_delay_secs = float(argv[2])

    presents, regions = load(fname)

    num_regions_completable = count_num_regions_completable(regions[:3], presents)
    print("Part 1:", num_regions_completable)

