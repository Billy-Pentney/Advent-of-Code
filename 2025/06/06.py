
import numpy as np

import regex as re

def load(fname):
    with open(fname, "r") as file:
        grid = [row.strip("\n") for row in file.readlines()]

    return grid

def compute_total_of_expressions(expressions):
    """
    Computes the value of each expression and sums their results.
    An expression is a pair, containing a list of integers and an operation which is applied to that list.
        e.g. ([5,2,3], *) is evaluated as 5*2*3 = 30
        
    :param expressions: A list of 2-tuples (numbers, op) where op is one of '*' or '+' and numbers is a list of integers.
    
    :return: the result of applying each operation to its corresponding list of numbers, and summing the results. 
    """

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



def find_total_solutions(grid):
    expressions = []
    rows = [re.split(" +", row.strip()) for row in grid]

    for x in range(len(rows[0])):
        ## Get all the cells in this column
        expression = [rows[y][x] for y in range(len(rows))]
        ## Parse all but the last value as an integer
        numbers = [int(x) for x in expression[:-1] if len(x) > 0]
        operation = expression[-1]
        expressions.append((numbers, operation))

    return compute_total_of_expressions(expressions)


def find_cephalopod_solutions(grid):
    col_widths = []
    operations_row = grid[-1]
    i = 0
    ## Find the width of each column by counting the spaces in the final row
    for j in range(len(operations_row)):
        if j == len(operations_row)-1:
            ## Add an additional space to include up to the end of the line
            col_widths.append(len(operations_row)+1-i)
        elif operations_row[j+1] in ["*", "+"]:
            col_widths.append(j+1-i)
            i = j+1
    
    ## Now, flip the data to order it by columns
    numbers_rows = grid[:-1]

    ## Store a list of the text in each column
    cols = [[] for _ in range(len(col_widths))]
    for row in numbers_rows:
        i = 0
        ## Select the text in this column on row i
        for j,w in enumerate(col_widths):
            cols[j].append(row[i:i+w-1])
            i += w

    ## Each list in cols is the column-ordered list of strings.
    ## But we need to decode each column, by reading its digits downwards.

    numbers_columns = []

    for i,col in enumerate(cols):
        ## Find the maximum width of any number in this column
        width = col_widths[i]

        decoded_col = []
        ## Use the right-to-left decoding
        for j in range(width-2,-1,-1):
            total = 0
            ## Read the jth digit in each number in this column
            for num in col:
                digit = num[j]
                if digit != ' ':
                    ## Add this as the least significant digit
                    total = total*10 + int(digit) 

            decoded_col.append(total)
        numbers_columns.append(decoded_col)

    ## Extract the operations for each column
    operations = re.split(" +", operations_row)
    ## Then merge the numbers lists for each column with its corresponding operation
    expressions = list(zip(numbers_columns, operations))

    return compute_total_of_expressions(expressions)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    grid = load(fname)

    total_solutions = find_total_solutions(grid)
    print(f"Part 1: {total_solutions}")

    total_cephalopod_solutions = find_cephalopod_solutions(grid)
    print(f"Part 2: {total_cephalopod_solutions}")
