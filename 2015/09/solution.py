import sys, os
import re


edge_re = re.compile("(\w+) to (\w+) = (\d+)")


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    adj_list = {}

    for line in lines:
        match = edge_re.match(line.strip("\n"))
        if match:
            start = match.group(1)
            end = match.group(2)
            cost = int(match.group(3))

            if start not in adj_list.keys():
                adj_list[start] = {}
            adj_list[start][end] = cost

            if end not in adj_list.keys():
                adj_list[end] = {}
            adj_list[end][start] = cost

    return adj_list


import numpy as np


def find_min_hamiltonian(curr, adj_list, seen):
    min_cost = 0
    nb_dict = adj_list[curr]

    for nb, cost in nb_dict.items():
        if nb in seen:
            continue
            
        ## Calculate the min hamiltonian from this neighbour
        next = seen.copy()
        next.add(nb)
        path_cost = cost + find_min_hamiltonian(nb, adj_list, next)

        if min_cost == 0 or path_cost < min_cost:
            min_cost = path_cost

        # print(" "*(len(seen)+1), nb, cost)

    return min_cost



## Solve Part One
def part_one(fileaddr):
    adj_list = read_file(fileaddr)
    print(adj_list.items())

    min_dist = None

    for start in adj_list.keys():
        seen = set()
        seen.add(start)
        dist = find_min_hamiltonian(start, adj_list, seen)
        if min_dist is None or dist < min_dist:
            min_dist = dist
        print(f"From {start}: {dist}")

    return min_dist


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
