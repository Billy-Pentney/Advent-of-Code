import sys, os
import re


def read_file(fileaddr):
    line = []
    with open(fileaddr, "r") as file:
        line = file.readline().strip("\n")
    return line



def rle(string):

    output = ""

    run = 1
    i = 0
    n = len(string)

    while i < n:
        if i < n-1 and string[i] == string[i+1]:
            run += 1
        else:
            output += str(run) + string[i]
            run = 1
        
        i += 1

    return output



## Solve Part One
def part_one(fileaddr, iters=1):
    line = read_file(fileaddr)
    result = line

    for iters in range(iters):
        result2 = rle(result)
        # print(f"{result} -> {result2}")
        result = result2

    return len(result)


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

    part_one_ans = part_one(fileaddr, 40)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    # part_two_ans = part_two(fileaddr)
    # print(f"(Part 2) Solution: {part_two_ans}")
