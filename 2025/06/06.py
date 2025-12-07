
import numpy as np

import regex as re

def load(fname):
    with open(fname, "r") as file:
        grid = [row for row in file.readlines()]

    return grid


def find_total_solutions(grid):
    expressions = []
    rows = [re.split(" +", row.strip("\n ")) for row in grid]

    for x in range(len(rows[0])):
        expression = [rows[y][x] for y in range(len(rows))]
        numbers = [int(x) for x in expression[:-1]]
        operation = expression[-1]
        expressions.append((numbers, operation))

    solutions = []

    for numbers, op in expressions:
        if op == '*':
            solution = np.prod(numbers, dtype=np.int64)
        elif op == '+':
            solution = np.sum(numbers, dtype=np.int64)
        else:
            print(f"Invalid operation '{op}'")
            continue

        solutions.append(solution)

    return np.sum(solutions)

def find_cephalopod_solutions(grid):
    ## todo
    pass



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)

    total_solutions = find_total_solutions(grid)
    print(f"Part 1: {total_solutions}")

    total_cephalopod_solutions = find_cephalopod_solutions(grid)
    print(f"Part 2: {total_cephalopod_solutions}")
