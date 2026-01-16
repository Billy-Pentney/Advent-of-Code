
import numpy as np
# import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    halves = []
    for line in lines:
        length = len(line)
        halves.append((line[:length//2], line[length//2:]))
    return halves

def get_priority(chr):
    val = ord(chr)
    if ord('a') <= val and val <= ord('z'):
        return 1 + val - ord('a')
    elif ord('A') <= val and val <= ord('Z'):
        return 27 + val - ord('A')
    return 0

def sum_priorities_shared(halves):
    shared_sum = 0
    for a,b in halves:
        shared = set(a).intersection(b)
        priorities = [get_priority(c) for c in list(shared)]
        # print(priorities)
        shared_sum += sum(priorities)
    return shared_sum


def sum_priorities_group_shared(halves):
    shared_group_sum = 0
    for i in range(0,len(halves),3):
        first = halves[i][0] + halves[i][1]
        second = halves[i+1][0] + halves[i+1][1]
        third = halves[i+2][0] + halves[i+2][1]
        print(first, second, third)
        common = set(first).intersection(second).intersection(third)
        priorities = [get_priority(c) for c in list(common)]
        shared_group_sum += sum(priorities)

    return shared_group_sum



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    halves = load(fname)
    part_one = sum_priorities_shared(halves)
    print("Part one:", part_one)
    part_two = sum_priorities_group_shared(halves)
    print("Part two:", part_two)
