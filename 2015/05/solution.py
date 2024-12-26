import sys, os
import re


def read_file(fileaddr):
    strings = []
    with open(fileaddr, "r") as file:
        strings = [line.strip("\n") for line in file.readlines()]
    
    return strings



def is_nice(string):
    excluded = ['ab', 'cd', 'pq', 'xy']
    for exc in excluded:
        if exc in string:
            return False
        
    consec_ltr = False
    vowels = 0

    for i,ltr in enumerate(string):
        if i > 0 and ltr == string[i-1]:
            consec_ltr = True
        
        if ltr in 'aeiou':
            vowels+=1

    return consec_ltr and vowels >= 3




## Solve Part One
def part_one(fileaddr):
    strings = read_file(fileaddr)

    """ 
        It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
        It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
        It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    """

    n_nice = 0
    for s in strings:
        if is_nice(s):
            print(f"{s} >> NICE")
            n_nice += 1    
        else:
            print(f"{s} >> X")    

    return n_nice


## Solve Part Two
def part_two(fileaddr):
    return










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    part_one_ans = part_one(fileaddr)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    # part_two_ans = part_two(fileaddr)
    # print(f"(Part 2) Solution: {part_two_ans}")
