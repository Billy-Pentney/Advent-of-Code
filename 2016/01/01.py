
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        instructions = np.array([row.strip("\n").split(", ") for row in file.readlines()]).flatten()

    return instructions

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

dir_to_vec = {
    NORTH: np.array([0, -1]),
    EAST: np.array([1, 0]),
    SOUTH: np.array([0, 1]),
    WEST: np.array([-1, 0])
}

def calculate_dist_from_start(instructions, start=(0,0), break_at_duplicate=False):
    seen = set()
    seen.add(start)
    start = np.array(start)
    curr = np.array(start)
    direction = NORTH

    for instruction in instructions:
        # print(curr, seen)
        # print(instruction)
        change = instruction[0]

        moves = int(str(instruction[1:]))
        if change == "R":
            direction = (direction + 1) % 4
        elif change == "L":
            direction = (3 + direction) % 4

        if not break_at_duplicate:
            ## Do all moves together (faster)
            curr += dir_to_vec[direction] * moves
        else:
            ## Store the new position after each move, for duplicate detection
            
            for i in range(moves):
                curr += dir_to_vec[direction]
                if tuple(curr) in seen:
                    # print(f"Revisited {curr}")
                    return np.linalg.norm(curr-start, ord=1)
                
                seen.add((int(curr[0]), int(curr[1])))

    ## Calculate L1-Norm, the distance from start to current
    return np.linalg.norm(curr-start, ord=1)


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    instructions = load(fname)
    part_one = calculate_dist_from_start(instructions)
    print("Part One: ", part_one)

    part_two = calculate_dist_from_start(instructions, break_at_duplicate=True)
    print("Part Two: ", part_two)