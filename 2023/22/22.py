import sys, os
import re



def coords_to_values(coords):
    splits = coords.split(",")
    return int(splits[0]), int(splits[1]), int(splits[2])


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    def line_to_brick(line):
        coords = line.replace("\n", "").split("~")
        # Get the points in x,y,z format
        return coords_to_values(coords[0]), coords_to_values(coords[1])
    
    return [line_to_brick(line) for line in lines]



def print_xz(grid, max_z=None):
    if max_z is None:
        max_z = len(grid[0][0])-1
    # print("  x  ")
    for z in range(max_z, -1, -1):
        row = []
        for x in range(len(grid)):
            curr = []
            for y in range(len(grid[0])):
                if len(curr) == 0:
                    curr.append(grid[x][y][z])
                elif grid[x][y][z] != '.' and grid[x][y][z] not in curr: 
                    if curr == ['.']:
                        curr = []
                    curr.append(grid[x][y][z])
            row.append("/".join(curr).rjust(10))        
        print(",".join(row),":", z)

def print_yz(grid, max_z=None):
    # print("  y  ")
    if max_z is None:
        max_z = len(grid[0][0])-1
    for z in range(max_z, -1, -1):
        row = []
        for y in range(len(grid[0])):
            curr = []
            for x in range(len(grid)):
                if len(curr) == 0:
                    curr.append(grid[x][y][z])
                elif grid[x][y][z] != '.' and grid[x][y][z] not in curr: 
                    if curr == ['.']:
                        curr = []
                    curr.append(grid[x][y][z])
            row.append("/".join(curr).rjust(10))
        print(",".join(row),":", z)


def populate_grid_with_bricks(bricks, grid, gravity=False):
    # For brick x, list all bricks which rely on x
    bricks_above = []
    # For brick x, list all bricks which x relies on 
    bricks_below = []

    max_z = 0
        
    for i, brick in enumerate(bricks):
        bricks_above.append(set())
        bricks_below.append(set())

        start = brick[0]
        end = brick[1]

        # Make the block fall, if this option was passed
        is_falling = gravity

        # Bottom of this block in the Z-axis
        z_start = min(start[2], end[2])
        # Height of this block in the Z-axis
        z_height = max(start[2], end[2])+1 - z_start

        while is_falling:
            for x in range(start[0], end[0]+1):
                for y in range(start[1], end[1]+1):
                    cell_under = grid[x][y][z_start-1]

                    if cell_under != '.':
                        # print(f"Brick {i} is supported at z={z_start-1}")
                        is_falling = False
                        if cell_under != '-':
                            bricks_above[int(cell_under)].add(i)
                            bricks_below[i].add(int(cell_under))
                        else:
                            # Bricks resting on the ground
                            bricks_below[i].add('-')


            if is_falling:
                # print(f"Falling z={z_start}")
                z_start -= 1
            else:
                max_z = max(max_z, z_start + z_height)
                # Write the brick to the grid
                for x in range(start[0], end[0]+1):
                    for y in range(start[1], end[1]+1):
                        for z in range(z_height):
                            grid[x][y][z_start+z] = str(i)
    
    return grid, bricks_above, bricks_below, max_z


def gen_grid(x_len, y_len, z_len):
    grid = []

    for x in range(x_len):
        ys = []
        for y in range(y_len):
            ys.append(['.' for z in range(z_len)])
        grid.append(ys)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y][0] = '-'

    return grid


def count_removable_bricks(bricks, bricks_above, bricks_below):
    num_removable = 0

    for i in range(0, len(bricks)):
        can_remove = True

        # For all bricks being supported by this brick
        for sup_brick in bricks_above[i]:
            # Check if at least one of them is only resting on this brick
            if len(bricks_below[sup_brick]) == 1:
                can_remove = False
                break
 
        if can_remove:
            # print("Can remove brick", i)
            num_removable += 1

    return num_removable



## Solve Part One
def part_one(fileaddr):
    bricks = read_file(fileaddr)
    # Sort by z-axis value of the lowest end of the brick
    # This is so that we can add the bricks in vertical order and apply gravity in one pass
    bricks.sort(key=lambda brick: min(brick[0][2], brick[1][2]))

    # Parameters are the max values of the data
    grid = gen_grid(x_len=10, y_len=10, z_len=330)

    # Add the bricks to the grid, with gravity
    grid, bricks_above, bricks_below, max_z = populate_grid_with_bricks(bricks, grid, gravity=True)

    print_xz(grid, max_z)

    return count_removable_bricks(bricks, bricks_above, bricks_below)


## Solve Part Two
def part_two(fileaddr):

    bricks = read_file(fileaddr)
    # Sort by z-axis value of the lowest end of the brick
    # This is so that we can add the bricks in vertical order and apply gravity in one pass
    bricks.sort(key=lambda brick: min(brick[0][2], brick[1][2]))

    # Parameters are the max values of the data
    grid = gen_grid(x_len=10, y_len=10, z_len=330)

    # Add the bricks to the grid, with gravity
    grid, bricks_above, bricks_below, max_z = populate_grid_with_bricks(bricks, grid, gravity=True)

    print("X-Z")
    print_xz(grid, max_z)
    print("Y-Z")
    print_yz(grid, max_z)
    
    collapses_if_removed = [0 for i in range(len(bricks))]

    # Brute-Force to find the number of collapses

    for i in range(len(bricks)-1, -1, -1):
        # print("Removing", str(i))
        removed = [i]
        bi = 0
        while bi < len(removed):
            curr = removed[bi]
            for sup_brick in bricks_above[curr]:
                if sup_brick in removed:
                    continue

                # Bricks still supporting sup_brick
                standing = [b for b in bricks_below[sup_brick] if b not in removed]
                # print(standing)

                if len(standing) == 0:
                    # print(f"Destroying brick {curr} causes brick {sup_brick} to collapse")
                    removed.append(sup_brick)
    
            bi+=1

        # Ignore the brick we removed to trigger the reaction
        collapses_if_removed[i] = len(removed)-1

    return sum(collapses_if_removed)










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
