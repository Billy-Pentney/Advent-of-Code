import sys, os
import re
from math import gcd


class Node:
    def __init__(self, name, left, right):
        self.name = name
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.name} -L-> {self.left}; -R-> {self.right})"




def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


def parse_node(line):
    ## Read a string of the form "XXX = (YYY, ZZZ)"

    pattern = "([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)"
    match = re.match(pattern, line)
    
    if match:
        source = match.group(1)
        left = match.group(2)
        right = match.group(3)
        return Node(source, left, right)



## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    instructions = lines[0].replace("\n", "")
    nodes = [parse_node(line) for line in lines[2:]]
    
    print(nodes)
    # print(instructions)

    node_map = {}
    for node in nodes:
        node_map[node.name] = node

    curr = "AAA"
    dest = "ZZZ"
    inst_i = 0

    steps = 0

    while curr != dest:
        if inst_i >= len(instructions):
            inst_i = 0

        if instructions[inst_i] == 'L':
            new_curr = node_map[curr].left
        elif instructions[inst_i] == 'R':
            new_curr = node_map[curr].right

        print(f"Moved: {curr} to {new_curr}")
        curr = new_curr

        steps += 1
        inst_i += 1

        if curr == dest:
            break

    return steps


def search_for_loop(history, new_move, num_insts):

    for i,move in enumerate(history):
        if move[0] == new_move[0] and move[1] % num_insts == new_move[1] % num_insts: 
            return move
        
    return None


def find_cycle(instructions, node_map, curr):
    steps = 0
    # history = [(curr, 0)]

    visited = {}

    inst_len = len(instructions)

    while True:
        inst = instructions[steps % inst_len]

        steps += 1

        if inst == 'L':
            new_node = node_map[curr].left
        elif inst == 'R':
            new_node = node_map[curr].right

        if (new_node in visited.keys()):
            # print(f"Revisited {new_node}")
            for visit_time in visited[new_node]:
                if visit_time % inst_len == steps % inst_len:
                    cycle_len = steps - visit_time
                    return (visit_time, cycle_len, new_node)
                
            visited[new_node].append(steps)
        else:
            visited[new_node] = [steps]

        curr = new_node

    return steps


def steps_to_reach_ending(instructions, node_map, curr: str, target_end: str):
    steps = 0
    inst_len = len(instructions)

    while not curr.endswith(target_end):
        inst_i = steps % inst_len
        if instructions[inst_i] == 'L':
            new_curr = node_map[curr].left
        elif instructions[inst_i] == 'R':
            new_curr = node_map[curr].right

        # print(f"Moved: {curr} to {new_curr}")
        curr = new_curr

        steps += 1
    
    return steps




def lcm(list):
    lcm = 1
    for i in list:
        lcm = lcm*i//gcd(lcm, i)
    return lcm




## Solve Part Two
def part_two(fileaddr):
    lines = read_file(fileaddr)

    instructions = lines[0].replace("\n", "")
    nodes = [parse_node(line) for line in lines[2:]]
    
    node_map = {}

    start_nodes = []
    steps_to_z = []

    for node in nodes:
        node_map[node.name] = node
        if node.name.endswith('A'):
            start_nodes.append(node.name)

    for node in start_nodes:
        # For each '..A' node, determine the number of steps required to reach the first '..Z' node 
        steps_req = steps_to_reach_ending(instructions, node_map, node, 'Z')
        print(f"  {node} requires {steps_req} steps to reach '..Z'")
        steps_to_z.append(steps_req)

    # Take the Lowest-Common-Multiple of the cycle lengths
    return lcm(steps_to_z)










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
