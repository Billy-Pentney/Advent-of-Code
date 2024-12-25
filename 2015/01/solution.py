import sys, os
import re


def read_file(fileaddr):
    line = []
    with open(fileaddr, "r") as file:
        line = file.readline().strip("\n")
    return line



## Solve Part One
def part_one(fileaddr):
    line = read_file(fileaddr)

    floor = 0
    for char in line:
        if char == '(':
            floor += 1
        elif char == ')':
            floor -= 1
    
    return floor


## Solve Part Two
def part_two(fileaddr):
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = 1
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)
    
    result = part_one(fileaddr)
    print(f"(Part 1) Result: {result}")
    
