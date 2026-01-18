
import numpy as np
from hashlib import md5
from queue import PriorityQueue
from collections import defaultdict
# import regex as re

def load(fname):
    with open(fname, "r") as file:
        passcodes = [it.strip("\n") for it in file.readlines()]
    return passcodes



"""

#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |  
####### V

The doors in your current room are either open or closed (and locked) based on the hexadecimal MD5 hash of a passcode (your puzzle input) followed by a sequence of uppercase characters representing the path you have taken so far (U for up, D for down, L for left, and R for right).

Only the first four characters of the hash are used; they represent, respectively, the doors up, down, left, and right from your current position. Any b, c, d, e, or f means that the corresponding door is open; any other character (any number or a) means that the corresponding door is closed and locked.
"""

chars_for_open = set(list("bcdef"))

def check_doors_open(route, passcode):
    hash_input = passcode + "".join(route)
    hash_res = md5(hash_input.encode()).hexdigest().lower()
    dirs = ['U','D','L','R']
    door_is_open = {
        d: hash_res[i] in chars_for_open
        for i,d in enumerate(dirs)
    }
    return door_is_open



def calc_heuristic(start, goal):
    return np.linalg.norm(np.array(start)-np.array(goal))

## Map each direction to its x-y vector
vecs = {'D':[0,1],'U':[0,-1],'R':[1,0],'L':[-1,0]}

MODE_SHORTEST = 'shortest'
MODE_LONGEST = 'longest'

def find_optimal_path(passcode, start=(0,0), goal=(3,3), mode=MODE_SHORTEST):
    frontier = PriorityQueue()
    frontier.put((0, start, []))
    n_rows, n_cols = goal[0]+1, goal[1]+1

    route_to_reach = { start: [] }

    while not frontier.empty():
        cost, curr, current_route = frontier.get()
        x,y = curr

        route_to_reach[curr] = current_route

        if curr == goal and mode == MODE_SHORTEST:
            ## Early exit, once find the optimal path
            break
        elif curr == goal:
            ## No early exit, keep exploring all options
            continue

        door_is_open = check_doors_open(current_route, passcode)

        for d,v in vecs.items():
            nx,ny = x+v[0],y+v[1]

            ## Skip any directions Out-of-Bounds or where the door isn't open
            if nx < 0 or ny < 0 or nx >= n_cols or ny >= n_rows or not door_is_open[d]:
                continue
            
            nb = (nx,ny)
            route_to_nb = current_route + [d]
            dist = len(current_route) + 1
            frontier.put((dist, nb, route_to_nb))

    if goal in route_to_reach:  
        path = "".join(route_to_reach[goal])  
        return path
    
    print("Error: goal not found!")
    return []



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    passcodes = load(fname)

    for passcode in passcodes:
        shortest_path = find_optimal_path(passcode)
        longest_path = find_optimal_path(passcode, mode=MODE_LONGEST)
        print(f"{passcode}")
        print(f"    Shortest: {shortest_path} (length={len(shortest_path)})")
        print(f"    Longest path: {len(longest_path)}")