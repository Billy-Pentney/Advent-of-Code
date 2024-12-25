import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines




## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    return


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
