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

    visited = set()

    x,y = 0,0
    for d in line:
        visited.add((x,y))
        if d == '^':
            y-=1
        elif d == '>':
            x+=1
        elif d == '<':
            x-=1
        elif d == 'v':
            y+=1
        

    return len(visited)


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

    unique_houses = part_one(fileaddr)
    print(f"(Part 1) Num unique houses: {unique_houses}")
    
