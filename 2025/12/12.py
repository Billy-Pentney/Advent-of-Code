
import numpy as np
import regex as re
from collections import namedtuple

Region = namedtuple("Region", ["width", "length", "reqs"])


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    presents = {}
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
            presents[present_num] = np.where(np.array(present) == '#', 1, 0)
            continue

        match_region = re.match("(\d+)x(\d+):((?: \d+)+)", line)
        if match_region:
            x = int(match_region.group(1))
            y = int(match_region.group(2))
            reqs = [int(x) for x in match_region.group(3).strip().split(" ")]
            regions.append(Region(x,y,reqs))

        i+=1

    return presents, regions

def print_grid(grid):
    print("")
    for y in range(grid.shape[0]):
        line = []
        for x in range(grid.shape[1]):
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
    return total_present_areas > grid_area
        
shape_rotations = {}


def try_placement(grid, presents, i, last_place=(0,0)):
    """
    Attempts to recursively place the remaining presents, starting at index i.
    Returns the grid after a successful placement of all remaining presents.
    
    :param grid: A 2D binary array in which the presents are to be placed.
    :param presents: A list of 2D binary arrays, indicating the shape of each present.
    :param i: The index of the first present yet to be placed.
    """
    if i >= len(presents):
        return grid

    present_idx = presents[i]
    present_rots = shape_rotations[present_idx]

    ## Check each 90 degree rotation
    for r,rot_shape in enumerate(present_rots):
        present_width = rot_shape.shape[0]
        present_height = rot_shape.shape[1]

        min_x = max(last_place[0]-present_width, 0)
        max_x = min(last_place[0]+present_width, grid.shape[0]-present_width)
        min_y = max(last_place[1]-present_height, 0)
        max_y = min(last_place[1]+present_height, grid.shape[1]-present_height)
        # min_x = 0
        # max_x = grid.shape[0]-present_width
        # min_y = 0
        # max_y = grid.shape[1]-present_height

        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                if i < 2:
                    print(f"Checking ({x},{y}) depth={i}, rot={r}")

                x2 = x + present_width
                y2 = y + present_height

                grid2 = grid.copy()
                ## Binary operation to mark the occupied cells
                grid2[x:x2,y:y2] = grid2[x:x2,y:y2] + rot_shape

                if i == 2:
                    print_grid(grid2)

                ## Count the number of cells with more than one shape
                if np.count_nonzero(grid2 > 1) > 0:
                    continue

                ## If no clashes, recurse on the remaining presents
                grid2 = try_placement(grid2, presents, i+1, (x,y))
                if grid2 is not None:
                    # print("Success")
                    return grid2

    return None



def check_region_suitability(region, presents):
    grid = np.full((region.width, region.length), 0)

    present_idxs = []
    for i,req in enumerate(region.reqs):
        for _ in range(req):
            present_idxs.append(i)

    if check_for_too_many_presents(grid, presents):
        return False

    output_grid = try_placement(grid, present_idxs, 0)
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
        for i,present in presents.items():
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

    presents, regions = load(fname)

    num_regions_completable = count_num_regions_completable(regions[:3], presents)
    print("Part 1:", num_regions_completable)

