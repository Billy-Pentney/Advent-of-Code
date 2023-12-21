import sys, os
import re
from queue import LifoQueue

part = '1'


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [list(line.replace("\n","")) for line in lines]



def print_grid(grid, as_string=False):
    for row in grid:
        if as_string:
            print("".join([str(x) for x in row]))
        else:
            print(row)


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def get_enterable_neighbours(lines, curr):
    nbs = []
    (row, col) = curr

    # Move North from current
    if row > 0:
        nbs.append((row-1, col))
    # Move East from current
    if col < len(lines[row])-1:
        nbs.append((row, col+1))
    # Move South from current
    if row < len(lines)-1:
        nbs.append((row+1, col))
    # Move West from current
    if col > 0:
        nbs.append((row, col-1))

    # print(nbs)
    
    return [nb for nb in nbs if lines[nb[0]][nb[1]] != '#']

def constrain_pt(nrows, ncols, pt):
    return ((pt[0] + nrows) % nrows, (pt[1] + ncols) % ncols)

def get_neighbours_wraparound(lines, curr):
    (row, col) = curr
    nbs = [
        (row-1, col), 
        (row, col+1),
        (row+1, col),
        (row, col-1)
    ]

    nrows = len(lines)
    ncols = len(lines[0])

    nbs = [(nb, constrain_pt(nrows, ncols, nb)) for nb in nbs]   

    return [(nb,cnb) for (nb,cnb) in nbs if lines[cnb[0]][cnb[1]] != '#']



reachable_in_steps = {}

def dfs(lines, stack, curr, remaining_steps, part='1'):

    if (curr, remaining_steps) in reachable_in_steps.keys():
        return reachable_in_steps[(curr, remaining_steps)]

    # print(stack)
    # prev = None
    # if len(stack) > 0:
    #     prev = stack[-1]

    if remaining_steps == 0:
        # Can't go any further on this branch
        return set([curr])

    reachable = set()

    new_stack = stack.copy()
    new_stack.append(curr)

    if part == '2':
        for nb, cnb in get_neighbours_wraparound(lines, curr):
            next_reachable = dfs(lines, new_stack, nb, remaining_steps-1, part)
            reachable = reachable.union(next_reachable)
    else:
        for nb in get_enterable_neighbours(lines, curr):
            next_reachable = dfs(lines, new_stack, nb, remaining_steps-1, part)
            reachable = reachable.union(next_reachable)
    
    # Backtrack, pop from queue
    reachable_in_steps[(curr, remaining_steps)] = reachable
    return reachable


def find_first_char(lines, char_to_find):
    for r, row in enumerate(lines):
        for c, char in enumerate(row):
            if char == char_to_find:
                return (c,r)

## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    start = find_first_char(lines, 'S')
    steps_req = 64
    can_reach = dfs(lines, [], start, steps_req)
    print(can_reach)

    for cell in can_reach:
        lines[cell[0]][cell[1]] = 'O'

    for line in lines:
        print("".join(line))

    return len(can_reach)


## Solve Part Two
def part_two(fileaddr):
    steps_req = 100 #26501365   

    lines = read_file(fileaddr)
    start = find_first_char(lines, 'S')
    can_reach = dfs(lines, [], start, steps_req, '2')
    print(can_reach)

    for cell in can_reach:
        lines[cell[0]][cell[1]] = 'O'

    for line in lines:
        print("".join(line))

    return len(can_reach)










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
    
