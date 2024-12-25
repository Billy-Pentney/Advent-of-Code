import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    boxes = []
    for line in lines:
        dims = [int(dim) for dim in line.strip("\n").split("x")]
        boxes.append(dims)

    return boxes



def calculate_paper(box):
    l,w,h = box[0], box[1], box[2]

    lw = l*w
    wh = w*h
    lh = l*h

    return 2*(lw+wh+lh) + min([lw,wh,lh])


## Solve Part One
def part_one(fileaddr):
    boxes = read_file(fileaddr)
    total_paper = sum([calculate_paper(box) for box in boxes])
    return total_paper

import numpy as np

def calculate_ribbon(box):
    volume = np.product(box)
    l,w,h = box[:3]
    min_perimeter = min(2*l+2*h, 2*l+2*w, 2*w+2*h)

    return min_perimeter + volume


## Solve Part Two
def part_two(fileaddr):
    boxes = read_file(fileaddr)
    return sum([calculate_ribbon(box) for box in boxes])










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(0)
    
    total_paper = part_one(fileaddr)
    print(f"(Part 1) Paper required: {total_paper}")
    
    total_ribbon = part_two(fileaddr)
    print(f"(Part 2) Ribbon required: {total_ribbon}")