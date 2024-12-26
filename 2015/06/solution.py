import sys, os
import re

pattern = re.compile("(on|off|flip) (\d+),(\d+),(\d+),(\d+)")


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()


    actions = []

    for line in lines:
        match = pattern.match(line)
        if match:
            instruction = match.group(1)
            x1 = int(match.group(2))
            y1 = int(match.group(3))
            x2 = int(match.group(4))
            y2 = int(match.group(5))
            actions.append({
                'instruction': instruction,
                'start': (x1,y1),
                'end': (x2,y2)
            })

    return actions


import numpy as np

## Solve Part One
def part_one(fileaddr):
    actions = read_file(fileaddr)

    grid = np.zeros((1000,1000), dtype='int')

    for action in actions:
        print(action)
        instruction = action['instruction']
        x1,y1 = action['start']
        x2,y2 = action['end']

        x2 = x2+1
        y2 = y2+1

        if instruction == 'off':
            grid[x1:x2,y1:y2] = 0
        elif instruction == 'on':
            grid[x1:x2,y1:y2] = 1
        elif instruction == 'flip':
            grid[x1:x2,y1:y2] = 1-grid[x1:x2,y1:y2]

    ## Count the number of 'on' lights
    return grid.sum()


## Solve Part Two
def part_two(fileaddr):
    actions = read_file(fileaddr)
    grid = np.zeros((1000,1000))

    for action in actions:
        print(action)
        instruction = action['instruction']
        x1,y1 = action['start']
        x2,y2 = action['end']

        x2 = x2+1
        y2 = y2+1

        if instruction == 'off':
            grid[x1:x2,y1:y2] = (grid[x1:x2,y1:y2]-1).clip(0)
        elif instruction == 'on':
            grid[x1:x2,y1:y2] += 1
        elif instruction == 'flip':
            grid[x1:x2,y1:y2] += 2

    return grid.sum()










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = int(args[1])
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    if part == 1:
        part_one_ans = part_one(fileaddr)
        print(f"(Part 1) Solution: {part_one_ans}")
    elif part == 2:
        part_two_ans = part_two(fileaddr)
        print(f"(Part 2) Solution: {part_two_ans}")
