import sys, os
import re

attribute_re = re.compile("(\w+): (\d+)")

def read_files():
    tape,sues = [],[]
    with open('tape.txt', "r") as file:
        tape = file.readlines()
    with open('sues.txt', "r") as file:
        sues = file.readlines()

    tape_results = {}
    for line in tape:
        splits = line.strip("\n").split(": ")
        name = splits[0]
        num = int(splits[1])
        tape_results[name] = num

    sue_objs = []
    for i,line in enumerate(sues):
        num = i+1
        sue = {'num': num}
        for match in attribute_re.findall(line):
            attr = match[0]
            count = int(match[1])
            sue[attr] = count
        sue_objs.append(sue)
    
    return tape_results, sue_objs




## Solve Part One
def part_one():
    tape, sues = read_files()
    print(tape)
    print(sues)

    candidates = []

    for sue in sues:
        is_candidate = True
        for attr, val in sue.items():
            if attr == 'num':
                continue
            if attr in tape.keys() and val != tape[attr]:
                is_candidate = False
                break
        if is_candidate:
            candidates.append(sue)


    # print("Candidates...")
    # for cand in candidates:
    #     print(" * "+str(cand))

    if len(candidates) > 0:
        print("Number of solutions:", len(candidates))
        return candidates[0]['num']
    else:
        return 0


## Solve Part Two
def part_two():
    tape, sues = read_files()
    # print(tape)
    # print(sues)

    candidates = []

    more_than_keys = ['cats', 'trees']
    less_than_keys = ['pomeranians', 'goldfish']
    exact_keys = ['children', 'samoyeds', 'akitas', 'vizslas', 'cars', 'perfumes']

    for sue in sues:
        is_candidate = True
        
        for attr in more_than_keys:
            if attr in sue.keys() and sue[attr] <= tape[attr]:
                is_candidate = False
                break

        for attr in less_than_keys:
            if attr in sue.keys() and sue[attr] >= tape[attr]:
                is_candidate = False
                break

        for attr in exact_keys:
            if attr in sue.keys() and sue[attr] != tape[attr]:
                is_candidate = False
                break

        if is_candidate:
            candidates.append(sue)

    if len(candidates) > 0:
        print("Number of solutions:", len(candidates))
        return candidates[0]['num']
    else:
        return 0










if __name__ == '__main__':
    part_one_ans = part_one()
    print(f"(Part 1) Solution: {part_one_ans}")
    part_two_ans = part_two()
    print(f"(Part 2) Solution: {part_two_ans}")
