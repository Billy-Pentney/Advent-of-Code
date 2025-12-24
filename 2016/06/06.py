
import numpy as np
from collections import defaultdict


def load(fname):
    with open(fname, "r") as file:
        rows = [list(row.strip("\n")) for row in file.readlines()]

    return np.array(rows)


def find_code(letters, part='1'):
    code = []
    for i in range(letters.shape[1]):
        col = letters[:,i]
        counts = defaultdict(lambda: 0)
        for ltr in col:
            counts[ltr] += 1

        # print(counts)
        sorted_counts = sorted(counts.keys(), key=lambda it: counts[it], reverse=True)
        
        if part == '1':
            ## Most common
            letter = sorted_counts[0]
        else:
            ## Least common
            letter = sorted_counts[-1]

        code.append(letter)
        
    return "".join(code)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    letters = load(fname)

    code_p1 = find_code(letters)
    print(f"Part one: {code_p1}") 
    code_p2 = find_code(letters, part='2')
    print(f"Part two: {code_p2}") 
