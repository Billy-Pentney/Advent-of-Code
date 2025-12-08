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


def find_hamiltonian_cost(curr, adj_list, seen, metric='min'):
    optimum_cost = 0
    nb_dict = adj_list[curr]

    for nb, cost in nb_dict.items():
        if nb in seen:
            continue
            
        ## Calculate the hamiltonian-path from this neighbour
        next = seen.copy()
        next.add(nb)
        path_cost = cost + find_hamiltonian_cost(nb, adj_list, next, metric)


        if optimum_cost == 0:
            optimum_cost = path_cost
        elif metric == 'min' and path_cost < optimum_cost:
            optimum_cost = path_cost
        elif metric == 'max' and path_cost > optimum_cost:
            optimum_cost = path_cost

        # print(" "*(len(seen)+1), nb, cost)

    return optimum_cost



## Solve Part One
def solve(fileaddr, part=1):
    adj_list = read_file(fileaddr)

    optimum_dist = None

    if part == 1:
        metric = 'min'
    else:
        metric = 'max'

    for start in adj_list.keys():
        seen = set()
        seen.add(start)
        dist = find_hamiltonian_cost(start, adj_list, seen, metric)

        if optimum_dist is None:
            optimum_dist = dist
        elif metric == 'min' and dist < optimum_dist:
            optimum_dist = dist
        elif metric == 'max' and dist > optimum_dist:
            optimum_dist = dist

        print(f" > {start}: {dist}")

    return optimum_dist







if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    part_one_ans = solve(fileaddr, part=1)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    part_two_ans = solve(fileaddr, part=2)
    print(f"(Part 2) Solution: {part_two_ans}")
