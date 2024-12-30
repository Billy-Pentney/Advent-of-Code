import sys, os
import re
import numpy as np


def read_file(fileaddr):
    buckets = []
    with open(fileaddr, "r") as file:
        buckets = [int(x.strip("\n")) for x in file.readlines()]
    return buckets


def recurse(buckets, capacity):
    if capacity < 0:
        return 0
    elif capacity == 0:
        return 1
    
    # depth = 4-len(buckets)
    
    num_ways = 0
    for i,bucket in enumerate(buckets):
        # print(" |"+"-"*depth,bucket)
        remaining_buckets = buckets[i+1:]
        remaining_capacity = capacity - bucket
        num_ways += recurse(remaining_buckets, remaining_capacity)

    return num_ways



## Solve Part One
def part_one(fileaddr, total=150):
    buckets = read_file(fileaddr)
    sorted_buckets = sorted(buckets, reverse=True)
    ways = recurse(sorted_buckets, total)
    return ways


## Solve Part Two
def part_two(fileaddr):
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    part_one_ans = part_one(fileaddr)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    # part_two_ans = part_two(fileaddr)
    # print(f"(Part 2) Solution: {part_two_ans}")
