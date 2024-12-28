import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = [l.strip("\n") for l in file.readlines()]
    return lines


from ast import literal_eval

## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)

    total_diff = 0

    for line in lines:
        code_length = len(line)
        str_length = len(literal_eval(line))
        diff = code_length - str_length
        print(f"{line}...".ljust(30), f"{code_length}-{str_length}={diff}".rjust(10))
        total_diff += diff

    return total_diff


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
