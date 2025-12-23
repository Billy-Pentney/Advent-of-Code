
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        triangles = [
            [int(side.strip()) for side in row.strip("\n").split(" ") if side.strip() != ''] 
            for row in file.readlines()
        ]

    return triangles

def count_valid(triangles):
    num_valid = 0
    for t in triangles:
        largest = max(t)
        others = sum(t) - largest
        if largest < others:
            print(f"{t} is valid!")
            num_valid += 1
    return num_valid

def count_valid_vertically(triangles):
    triangles = np.array(triangles)
    num_valid = 0
    for i in range(0, triangles.shape[0], 3):
        for x in range(3):
            t = triangles[i:i+3,x]
            # print(t)
            largest = max(t)
            others = sum(t) - largest
            if largest < others:
                print(f"{t} is valid!")
                num_valid += 1
    return num_valid



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    triangles = load(fname)
    num_valid = count_valid(triangles)
    print(f"Part one: {num_valid}")    
    num_valid_vertically = count_valid_vertically(triangles)
    print(f"Part two: {num_valid_vertically}")