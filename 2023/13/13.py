import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return [line.replace("\n", "") for line in lines]



def num_differences(col1, col2):
    # Assume len(col1) == len(col2)
    num_diffs = 0

    for i in range(0, len(col1)):
        if col1[i] != col2[i]:
            num_diffs += 1
    
    return num_diffs


def find_reflection_line(cols):
    num_cols = len(cols)

    for i in range(0, num_cols-1):
        # Consider the line between i and i+1
        reflection = True
        j = i
        k = i+1

        differences_count = 0

        while j >= 0 and k <= num_cols-1:
            differences_count += num_differences(cols[j], cols[k])
            j -= 1
            k += 1
            if differences_count > 0:
                reflection = False
                break

        if reflection:
            return (i,i+1)
            
    return None


def find_smudged_reflection_line(cols):
    num_cols = len(cols)

    main_line = None
    smudge_line = None

    for i in range(0, num_cols-1):
        # Consider the line between i and i+1
        j = i
        k = i+1

        differences_count = 0

        while j >= 0 and k <= num_cols-1:
            differences_count += num_differences(cols[j], cols[k])
            j -= 1
            k += 1
            if differences_count > 1:
                break

        if differences_count == 0:
            main_line = (i,i+1)
        elif differences_count == 1:
            smudge_line = (i,i+1)
            
    return smudge_line       


        

def score_pattern(pattern_rows, part='1'):
    # print(pattern_rows)

    cols = []

    ## Convert to column-indexed list
    for i in range(0, len(pattern_rows[-1])):
        col = ""
        for row in pattern_rows:
            col += row[i]
        cols.append(col)

    # print(cols)
    if part == '1':
        vl = find_reflection_line(cols)
    elif part == '2':
        vl = find_smudged_reflection_line(cols)

    if vl is not None:
        print("Vertical:", vl)
        return (vl[0]+1)
    
    if part == '1':
        hl = find_reflection_line(pattern_rows)
    elif part == '2':
        hl = find_smudged_reflection_line(pattern_rows)

    print("Horizontal:", hl)
    return 100 * (hl[0]+1)




## Solve Part One
def sum_reflection_scores(fileaddr, part='1'):
    all_rows = read_file(fileaddr)

    patterns = []
    pattern = []

    # Split at empty lines
    for row in all_rows:
        if len(row) > 0:
            pattern.append(row)
        else:
            patterns.append(pattern)
            pattern = []

    if len(pattern) > 0:
        patterns.append(pattern)

    scores = [score_pattern(p, part) for p in patterns]

    return sum(scores)






if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        result = sum_reflection_scores(fileaddr, part)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
