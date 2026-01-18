import sys, os
import re


def find_all_galaxies(lines):
    galaxies = []
    by_col = []
    by_row = []

    # Prepopulate columns, so we can add as necessary
    for col in range(0, len(lines[0])):
        by_col.append([])

    for row, line in enumerate(lines):
        by_row.append([])
        for col, char in enumerate(line):
            if char == '#':
                galaxy = (row,col)
                i = len(galaxies)
                galaxies.append(galaxy)
                by_row[row].append(i)
                by_col[col].append(i)
    
    return galaxies, by_row, by_col



def sum_shortest_paths(fileaddr, part='1'):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    galaxies, by_row, by_col = find_all_galaxies(lines)

    n = len(galaxies)

    # Each empty column/row is extended by this number
    expansion_gap = 1
    if part == '2':
        expansion_gap = 999999

    sum_dist = 0

    ## Consider each pair of galaxies
    for j in range(0, n):
        for i in range(0, j):
            (r1,c1) = galaxies[i]
            (r2,c2) = galaxies[j]

            hdist = abs(c2-c1)
            for c in range(min(c1,c2),max(c1,c2)):
                # For each column which has no galaxies
                if len(by_col[c]) == 0:
                    hdist += expansion_gap
            
            vdist = abs(r2-r1)
            for r in range(min(r1,r2),max(r1,r2)):
                # For each row which has no galaxies
                if len(by_row[r]) == 0:
                    vdist += expansion_gap

            dist = hdist + vdist
            # print(f"Galaxy {i+1} to Galaxy {j+1} is distance {dist}")
        
            sum_dist += dist

    return sum_dist
    










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        result = sum_shortest_paths(fileaddr, part)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
