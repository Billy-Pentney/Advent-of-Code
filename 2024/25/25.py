
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = [list(row.strip("\n")) for row in file.readlines()]

    keys = []
    locks = []

    blocks = []
    block = []
    for line in lines:
        if len(line) == 0:
            blocks.append(block)
            block = []
        else:
            block.append(line)
    if len(block) > 0:
        blocks.append(block)

    for block in blocks:
        ## Locks have the top-row filled with '#' and the bottom-row empty '.'
        ## Keys have the opposite.

        is_lock = '#' in block[0]
        
        blk = np.array(block)

        ## Count the number of filled cells in each column
        blk_heights = np.sum(blk=='#', axis=0)-1
        # for row in blk:
        #     print("".join(row))

        if is_lock:
            locks.append(blk_heights)
            # print(f"Lock: {blk_heights}")
        else:
            keys.append(blk_heights)
            # print(f"Key: {blk_heights}")

    return locks, keys


def check_fit(lock, key, depth=5):
    for i in range(len(key)):
        if lock[i] > depth-key[i] or key[i] > depth-lock[i]:
            return False
    return True


def part_one(locks, keys, print_matches=False):
    n_potential_matches = 0

    for lock in locks:
        for key in keys:
            if check_fit(lock, key):
                if print_matches:
                    print(f"Lock {lock} matched with {key}")
                n_potential_matches += 1

    return n_potential_matches




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    locks,keys = load(fname)

    n_potential_matches = part_one(locks, keys, print_matches=len(locks) < 10)
    print(f"(Part 1) Num Potential Matches: {n_potential_matches}")