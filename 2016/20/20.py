
import numpy as np
import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    blocklist = []
    for line in lines:
        splits = line.split("-")
        from_num = int(splits[0])
        to_num = int(splits[1])
        blocklist.append((from_num, to_num))

    blocklist = sorted(blocklist)

    ## Compress the blocklist by merging consecutive/overlapping ranges
    blocklist_efficient = []
    blocklist_efficient.append(blocklist[0])
    for i in range(1, len(blocklist)):
        from1,to1 = blocklist_efficient[-1]
        from2,to2 = blocklist[i]
        if to1+1 >= from2:
            blocklist_efficient[-1] = (from1, max(to1,to2))
        else:
            blocklist_efficient.append(blocklist[i])

    return blocklist_efficient

def find_lowest_allowed(blocklist):
    candidate = 0
    for (from_num, to_num) in blocklist:
        print(f"Comparing {candidate} to range {from_num}-{to_num}")
        if candidate < from_num:
            return candidate
        else:
            candidate = max(candidate, to_num+1)

    return candidate

## 2^32 - 1 
MAX_IP = 4294967295

def count_allowed(blocklist):
    num_allowed = 0
    first_allowed = 0

    for (from_num, to_num) in blocklist:
        if first_allowed > to_num:
            continue
        print(f"Comparing {first_allowed} to range {from_num}-{to_num}")
        if first_allowed < from_num:
            num_allowed += from_num - first_allowed
            print(f"Num allowed {num_allowed}")
        first_allowed = max(first_allowed, to_num+1)

    if first_allowed < MAX_IP:
        num_allowed += MAX_IP - first_allowed

    return num_allowed


from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    blocklist = load(fname)
    lowest_allowed_ip = find_lowest_allowed(blocklist)
    print("Part one:", lowest_allowed_ip)
    num_allowed_ips = count_allowed(blocklist)
    print("Part two:", num_allowed_ips)
