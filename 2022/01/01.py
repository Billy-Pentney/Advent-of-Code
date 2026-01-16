
import numpy as np
# import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        weights = [row.strip("\n") for row in file.readlines()]

    elves = []
    curr_elf = []
    for w in weights:
        if len(w) == 0:
            elves.append(curr_elf)
            curr_elf = []
        else:
            curr_elf.append(int(w))
    if curr_elf:
        elves.append(curr_elf)

    return elves


def find_max_weight_carried(elves, n_top=1):
    total_weights = [
        sum(elf) for elf in elves
    ]
    top_elves = sorted(total_weights, reverse=True)[:n_top]
    return sum(top_elves)


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    elves = load(fname)
    # print(elves)
    part_one = find_max_weight_carried(elves)
    print("Part one:", part_one)
    part_two = find_max_weight_carried(elves, 3)
    print("Part two:", part_two)
