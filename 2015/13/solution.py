import sys, os
import re

## Frank would lose 92 happiness units by sitting next to Mallory.
happiness_re = re.compile("(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+).")


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    adj_list = {}

    for line in lines:
        match = happiness_re.match(line.strip("\n"))
        if match:
            first = match.group(1)
            sentiment = match.group(2)      ## gain or lose
            amount = int(match.group(3))
            if sentiment == 'lose':
                amount *= -1
            
            second = match.group(4)
            if first not in adj_list:
                adj_list[first] = {}

            adj_list[first][second] = amount

    return adj_list


def eval_allocation(alloc, happiness):
    """
        Compute the total happiness under the given allocation of people to seats.

        Params
        ---
        alloc: list[str]
            A list of names, whose index indicates the seat number. Adjacent names in the list are seated next to each other.
        happiness: dict[str, dict[str, int]]
            A dictionary of the names which maps a name X to another dictionary with names Y which describes the gain in happiness if Y is sat next to X.
    
        Returns
        ---
        The total happiness of all individuals in the given allocation

    """
    n = len(alloc)
    total_happiness = 0
    for i in range(n):
        prev = alloc[(i-1+n) % n]
        curr = alloc[i]
        next = alloc[(i+1) % n]

        total_happiness += happiness[curr][prev]
        total_happiness += happiness[curr][next]

    return total_happiness
        

import numpy as np


def greedy_allocate(alloc, i, adj_list):
    if i == len(alloc):
        return eval_allocation(alloc, adj_list)
    
    best_alloc = 0
    
    alloc_2 = alloc.copy()

    for name in adj_list.keys():
        if name in alloc:
            ## Already seated
            continue
        
        # print("--"*i + name)

        alloc_2[i] = name
        ## Recurse to find the best allocation
        alloc_2_eval = greedy_allocate(alloc_2, i+1, adj_list)

        if alloc_2_eval > best_alloc:
            best_alloc = alloc_2_eval

    return best_alloc


    



    




## Solve Part One
def part_one(fileaddr):
    happiness = read_file(fileaddr)

    n = len(happiness.keys())
    alloc = ['' for i in range(n)]
    best_happiness = greedy_allocate(alloc, 0, happiness)

    return best_happiness


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
