import sys, os
import re

num_regex = re.compile("(\-?\d+)")


def read_file(fileaddr):
    text = []
    with open(fileaddr, "r") as file:
        text = file.read()
    return text




## Solve Part One
def part_one(fileaddr):
    text = read_file(fileaddr)
    total = 0

    for match in num_regex.findall(text):
        num = int(match)
        # print(num)
        total += num

    return total


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
