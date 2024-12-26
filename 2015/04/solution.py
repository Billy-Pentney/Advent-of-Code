import sys, os
import re
import hashlib

MAX_ITER = 10000000


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines[0].strip("\n")


def find_md5_with_zero_prefix(base, n_zeros=5, max_iter=MAX_ITER):
    prefix = '0'*n_zeros

    for i in range(1, max_iter):
        input_str = base + str(i)
        hash = hashlib.md5(input_str.encode())

        hex_hash = hash.hexdigest()
        if hex_hash.startswith(prefix):
            print(f"Found MD5 with {n_zeros}-zero prefix...")
            print(f" >> MD5({input_str}) = {hex_hash}")

            return i
        
    print(f"No solutions in first {max_iter} iterations!")
    return None



## Solve Part One
def part_one(fileaddr, max_iter=1000000):
    line = read_file(fileaddr)  
    return find_md5_with_zero_prefix(line, 5, max_iter)


## Solve Part Two
def part_two(fileaddr, max_iter=MAX_ITER):
    line = read_file(fileaddr)
    return find_md5_with_zero_prefix(line, 6, max_iter)






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
