
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    fresh_ranges = []
    ingredients = set()

    blank_line_seen = False

    for line in lines:
        if len(line) == 0:
            blank_line_seen = True
        elif blank_line_seen:
            ingredients.add(int(line))
        else:
            ranges = line.split("-")
            start = ranges[0]
            end = ranges[1]
            fresh_ranges.append([int(start), int(end)])

    return (fresh_ranges, ingredients)

def count_num_fresh(fresh_ranges, ingredients: set):
    is_fresh = set()

    for r in fresh_ranges:
        start,end = r[0],r[1]
        # print(f"Checking range {start}-{end}")
        ## Find all ingredients in this range
        new_fresh = [i for i in ingredients if start <= i and i <= end]
        is_fresh = is_fresh.union(new_fresh)

    # for ingredient in ingredients:
    #     if ingredient in is_fresh:
    #         print(f"{ingredient} is fresh!")
    #     else:
    #         print(f"{ingredient} is old!")

    return len(is_fresh)



def count_all_fresh(fresh_ranges):
    ## Sort the ranges, by start, then by end
    fresh_ranges = sorted(fresh_ranges, key=lambda x: (x[0], x[1]))

    ## Now we need to combine adjacent/overlapping ranges to avoid counting duplicates
    fresh_ranges2 = [fresh_ranges[0]]

    ## Merge the consecutive/overlapping ranges
    for i in range(1, len(fresh_ranges)):
        fr1 = fresh_ranges2[-1]
        fr2 = fresh_ranges[i]

        ## Check for overlap or consecutive ranges 
        if fr1[1] >= fr2[0] - 1:
            ## If so, then choose the largest range
            fr1[1] = max(fr1[1], fr2[1])
        else:
            ## Otherwise, just add it as the latest range
            fresh_ranges2.append(fr2)

    ## Count the width of each range
    total_fresh = sum([end+1-start for (start,end) in fresh_ranges2]) 

    return total_fresh


from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    fresh_ranges, ingredients = load(fname)

    num_fresh = count_num_fresh(fresh_ranges, ingredients)
    print(f"Part 1: {num_fresh}")

    total_fresh = count_all_fresh(fresh_ranges)
    print(f"Part 2: {total_fresh}")
