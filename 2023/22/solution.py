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


def print_xz(grid):
    # print("  x  ")
    for z in range(len(grid[0][0])-1, -1, -1):
        row = "  "
        for x in range(len(grid)):
            curr = '.'
            for y in range(len(grid[0])):
                if grid[x][y][z] != '.':
                    curr = grid[x][y][z]
            row += curr
        print(row)

def print_yz(grid):
    # print("  y  ")
    for z in range(len(grid[0][0])-1, -1, -1):
        row = "  "
        for y in range(len(grid[0])):
            curr = '.'
            for x in range(len(grid)):
                if grid[x][y][z] != '.':
                    curr = grid[x][y][z]
            row += curr
        print(row)


## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    grid = []
    
    x_len = 10
    y_len = 10
    z_len = 500

    for x in range(x_len):
        ys = []
        for y in range(y_len):
            ys.append(['.' for z in range(z_len)])
        grid.append(ys)

    for x in range(len(grid)):
        for y in range(len(grid[0])):
            grid[x][y][0] = '-'

    bricks = []

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

        supporting[i] = []
        supported_by[i] = []

        z_start = min(start[2], end[2])
        z_len = end[2]+1-start[2]
        # Make the block fall
        is_falling = True

        while is_falling:
            for x in range(start[0], end[0]+1):
                for y in range(start[1], end[1]+1):
                    cell_under = grid[x][y][z_start-1]
                    if cell_under != '.':
                        print(f"Found brick at {z_start-1}")
                        is_falling = False
                        supporting[cell_under].append(i)
                        supported_by[i].append(cell_under)

            if is_falling:
                z_start -= 1
                print(f"Brick {i} fell 1 block")

        for x in range(start[0], end[0]+1):
            for y in range(start[1], end[1]+1):
                for zi in range(z_len):
                    grid[x][y][z_start+zi] = str(i)

    # print("\nX-Z View:")
    # print_xz(grid)
    # print("\nY-Z View:")
    # print_yz(grid)

    num_removable = 0

    # print(supporting)

    for i in range(0, len(bricks)):
        B = bricks[i]
        can_remove = True

        for sup_brick in supporting[i]:
            # Check if at least one brick resting on B, is only resting on B
            if len(supported_by[sup_brick]) == 1:
                can_remove = False
                break
 
        if can_remove:
            print("Can remove brick", i)
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
    
