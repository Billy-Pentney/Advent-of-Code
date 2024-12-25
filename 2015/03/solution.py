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


def move(x,y,d):
    if d == '^':
        return x,y-1
    elif d == '>':
        return x+1,y
    elif d == '<':
        return x-1,y
    elif d == 'v':
        return x,y+1


## Solve Part Two
def part_two(fileaddr):
    line = read_file(fileaddr)

    visited1 = set()
    visited2 = set()

    x1,y1 = 0,0
    x2,y2 = 0,0

    for i in range((len(line)+1)//2):
        d1 = line[2*i]
        visited1.add((x1,y1))
        x1,y1 = move(x1,y1,d1)

        if 2*i+1 < len(line):
            d2 = line[2*i+1]
            visited2.add((x2,y2))
            x2,y2 = move(x2,y2,d2)

    visited1.add((x1,y1))
    visited2.add((x2,y2))

    visited = visited1.union(visited2)
    # print(visited)
    return len(visited)










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
    
    unique_houses_two = part_two(fileaddr)
    print(f"(Part 2) Num unique houses with two santas: {unique_houses_two}")
    