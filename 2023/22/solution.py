import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]


def coords_to_values(coords):
    splits = coords.split(",")
    return int(splits[0]), int(splits[1]), int(splits[2])


def print_xz(grid, max_z=None):
    if max_z is None:
        max_z = len(grid[0][0])-1
    # print("  x  ")
    for z in range(max_z, -1, -1):
        row = []
        for x in range(len(grid)):
            curr = []
            for y in range(len(grid[0])):
                if grid[x][y][z] == '.':
                    continue
                if len(curr) == 0 or grid[x][y][z] not in curr: 
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
                if grid[x][y][z] == '.':
                    continue
                if len(curr) == 0 or grid[x][y][z] not in curr: 
                    curr.append(grid[x][y][z])
            row.append("/".join(curr).rjust(10))
        print(",".join(row),":", z)


## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    grid = []
    
    x_len = 10
    y_len = 10
    z_len = 330

    for x in range(x_len):
        ys = []
        for y in range(y_len):
            ys.append(['.' for z in range(z_len)])
        grid.append(ys)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y][0] = '-'

    bricks = []

    max_z = 0

    # For brick x, list all bricks which rely on x for support
    supporting = {}
    # For brick x, list all bricks which x relies on 
    supported_by = {}

    # Track bricks resting on the base
    supporting['-'] = []

    for i,line in enumerate(lines):
        coords = line.split("~")
        # Get the points in x,y,z format
        start = coords_to_values(coords[0])
        end = coords_to_values(coords[1])

        bricks.append((start,end))

    # Sort by z-axis value of the lowest end of the brick
    bricks.sort(key=lambda brick: min(brick[0][2], brick[1][2]))
    # bricks = bricks[:6]

    for i, brick in enumerate(bricks):
        start,end = brick
        # print(f"{i}: {brick}")
        z_start = min(start[2], end[2])
        z_len = end[2]+1-start[2]
        supporting[str(i)] = []
        supported_by[str(i)] = []

        # Make the block fall
        is_falling = True

        while is_falling:
            for x in range(start[0], end[0]+1):
                for y in range(start[1], end[1]+1):
                    cell_under = grid[x][y][z_start-1]
                    if cell_under != '.':
                        # print(f"Brick {i} is supported at z={z_start-1}")
                        is_falling = False
                        supporting[cell_under].append(str(i))
                        supported_by[str(i)].append(cell_under)

            if is_falling:
                z_start -= 1
            else:
                print(f"Brick {i} fell {min(end[2]+1-start[2],z_start)} block/s")

        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                for zi in range(z_len):
                    grid[x][y][z_start+zi] = str(i)
                max_z = max(max_z, z_start+z_len)

    # print("\nX-Z View:")
    # print_xz(grid, max_z)
    # print("\nY-Z View:")
    # print_yz(grid, max_z)

    num_removable = 0

    # print(supporting)

    for i in range(0, len(bricks)):
        can_remove = True

        for sup_brick in supporting[str(i)]:
            # Check if at least one brick resting on B, is only resting on B
            if len(supported_by[sup_brick]) == 1:
                can_remove = False
                break
 
        if can_remove:
            # print("Can remove brick", i)
            num_removable += 1

    return num_removable


## Solve Part Two
def part_two(fileaddr):
    return










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
    
