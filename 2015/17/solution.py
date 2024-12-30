import sys, os
import re
import numpy as np


def read_file(fileaddr):
    buckets = []
    with open(fileaddr, "r") as file:
        buckets = [int(x.strip("\n")) for x in file.readlines()]
    return buckets


def find_ways(buckets, capacity, used):
    """
        Recursively compute all unique subsets of buckets which sum to the given capacity, while using the used list.
        Returns a list of valid combinations of buckets.
    """
    if capacity < 0:
        return []
    elif capacity == 0:
        return [used]
        
    ways = []
    for i,bucket in enumerate(buckets):
        # print(" |"+"-"*depth,bucket)
        remaining_buckets = buckets[i+1:]
        new_used = used.copy()
        new_used.append(bucket)
        remaining_capacity = capacity - bucket
        new_ways = find_ways(remaining_buckets, remaining_capacity, new_used)
        ways.extend(new_ways)
        
    return ways






## Solve Part One
def part_one(fileaddr, total=150):
    buckets = read_file(fileaddr)
    sorted_buckets = sorted(buckets, reverse=True)
    ways = find_ways(sorted_buckets, total, used=[])
    return len(ways)


## Solve Part Two
def part_two(fileaddr, total=150):
    buckets = read_file(fileaddr)
    sorted_buckets = sorted(buckets, reverse=True)
    ways = find_ways(sorted_buckets, total, used=[])

    lengths = [len(way) for way in ways]
    min_len = min(lengths)
    
    return sum([1 for len in lengths if len == min_len])










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    total = 150

    part_one_ans = part_one(fileaddr, total)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    part_two_ans = part_two(fileaddr, total)
    print(f"(Part 2) Solution: {part_two_ans}")
