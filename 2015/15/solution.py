import sys, os
import re


ingredient_re = re.compile("(\w+): capacity (\-?\d+), durability (\-?\d+), flavor (\-?\d+), texture (\-?\d+), calories (\-?\d+)")

import numpy as np

def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    ingredients = {}

    for line in lines:
        match = ingredient_re.match(line.strip("\n"))
        if match:
            name = match.group(1)
            attrs = np.zeros(5)
            
            ## capacity
            attrs[0] = int(match.group(2))
            ## durability
            attrs[1] = int(match.group(3))
            ## flavor
            attrs[2] = int(match.group(4))
            ## texture
            attrs[3] = int(match.group(5))
            ## calories
            attrs[4] = int(match.group(6))

            ingredients[name] = attrs

    return ingredients


def find_max_score(ingredients, alloc, remaining, attrs, req_calories=None, verbose=False):
    i = len(alloc)
    if i >= len(ingredients):
        return 0
    
    ingredient = ingredients[i]

    if i == len(ingredients) - 1:
        ## This is the last ingredient, so we must use the remaining amount
        amt = remaining
        alloc = alloc.copy()
        alloc.append(amt)
        recurse_score = attrs + (ingredient*amt)
        sum = np.product(np.clip(recurse_score[:4], 0, None))
        if verbose and sum > 0:
            print(" * ", alloc, "...", sum)
        if req_calories is None or recurse_score[4] == req_calories:
            return sum
        return 0

    max_sum = 0

    for amt in range(remaining+1):
        ## Use this ingredient amt times
        ## This is a 5-vector containing the total weighted score of the attributes of these cookies 
        recurse_score = attrs + (ingredient*amt)
        alloc_2 = alloc.copy()
        alloc_2.append(amt)

        if req_calories is not None and recurse_score[4] > req_calories:
            ## Skip as we've exceeded the calorie target
            continue

        recurse_sum = find_max_score(ingredients, alloc_2, remaining-amt, recurse_score, req_calories, verbose)

        ## Take the highest sum
        if recurse_sum > max_sum:
            max_sum = recurse_sum

    return max_sum





## Solve Part One
def part_one(fileaddr):
    ingredients = read_file(fileaddr)

    for name, attrs in ingredients.items():
        print(name, ":", attrs)

    ingredient_list = list(ingredients.values())
    return int(find_max_score(ingredient_list, [], 100, attrs=np.zeros(5), req_calories=None, verbose=False))


## Solve Part Two
def part_two(fileaddr):
    ingredients = read_file(fileaddr)
    for name, attrs in ingredients.items():
        print(name, ":", attrs)

    ingredient_list = list(ingredients.values())
    return int(find_max_score(ingredient_list, [], 100, attrs=np.zeros(5), req_calories=500, verbose=False))









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
