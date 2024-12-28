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


def run_rle_iters(string, iters=1, verbose=False):
    result = string

    for i in range(iters):
        result2 = rle(result)
        # print(f"{result} -> {result2}")
        result = result2
        if verbose:
            print(f"After iter {i+1}, length={len(result)}")

    return len(result)



## Solve Part One
def part_one(fileaddr):
    line = read_file(fileaddr)
    return run_rle_iters(line, 40)


## Solve Part Two
def part_two(fileaddr):
    line = read_file(fileaddr)
    return run_rle_iters(line, 50, verbose=True)










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
    
    part_two_ans = part_two(fileaddr)
    print(f"(Part 2) Solution: {part_two_ans}")
