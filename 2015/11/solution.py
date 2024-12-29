import sys, os
import re


def read_file(fileaddr):
    line = []
    with open(fileaddr, "r") as file:
        line = file.readline().strip("\n")
    return line


import numpy as np

DISALLOWED_NUMS = [ord(ltr) for ltr in 'iol']

def inc_num_password(pword, length=8):

    carry = True
    i = length-1
    new_pword = np.array(pword)

    while i < len(pword) and carry:
        last_num = pword[i]
        last_new_num = (last_num + 1) % 26

        ## Skip any disallowed letters
        while last_new_num in DISALLOWED_NUMS:
            last_new_num = (last_new_num + 1) % 26

        new_pword[i] = last_new_num

        ## Check if we wrapped the digit
        carry = last_new_num < last_num
        i -= 1
    
    return new_pword[-8:]



def check_valid(numeric_pword):

    """
    Passwords must:
        * include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
        * not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
        * contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
    """

    disallowed = [ord('i'), ord('o'), ord('l')]

    n = len(numeric_pword)
    triple_found = False

    # Store the starting index of each double-letter pair
    # e.g. "abccdeeef" has pairs = { 'cc':2, 'ee':5 }
    pairs = {}
    double_pair = False

    for i in range(n):
        ## Check for a triple of ascending letters, e.g. 'abc'
        if i < n-2 and not triple_found and numeric_pword[i]+1 == numeric_pword[i+1] and numeric_pword[i]+2 == numeric_pword[i+2]:
            triple_found = True

        ## Check for a pair of the same letter
        if i < n-1 and not double_pair and numeric_pword[i] == numeric_pword[i+1]:
            pair = chr(numeric_pword[i]+ord('a'))*2
            if pair in pairs.keys() and pairs[pair] < i-1:
                ## Two of the same pair but not overlapping
                double_pair = True
            else:
                # Store the starting index of this pair
                pairs[pair] = i
                if len(pairs) >= 2:
                    double_pair = True
        
        ## Check for disallowed letters
        if numeric_pword[i] in disallowed:
            return False

    return triple_found and double_pair
            


def to_ord(pword):
    ord_arr = np.full(len(pword), 0)
    for i,ltr in enumerate(pword):
        ## Convert from a letter in a-z to an index in 0-25
        ord_arr[i] = ord(ltr)-ord('a')
    return ord_arr

def to_chars(ord_arr):
    pword = np.full(len(ord_arr), 'x')
    for i, ltr_index in enumerate(ord_arr):
        # Convert from index 0-25 to a letter in a-z
        pword[i] = chr(ltr_index+ord('a'))
    return pword



## Solve Part One
def part_one(fileaddr):
    pword = read_file(fileaddr)
    pword_num = to_ord(pword)
    # print(pword_num)
    i = 0
    # print("".join(pword))

    max_iters = 1000000
    printerval = 20000

    keep_incrementing = True

    while keep_incrementing:
        new_pword_num = inc_num_password(pword_num)
        new_pword = to_chars(new_pword_num)

        new_pword_joined = "".join(new_pword)

        ## Print every kth password
        if i % printerval == 0:
            print(f" -> {new_pword_joined}")

        pword_num = new_pword_num
        pword = new_pword
        i+=1
        keep_incrementing = not check_valid(pword_num) and i < max_iters

    if not check_valid(pword_num):
        print("Iteration limit reached!")
        return None

    return "".join(pword)


## Solve Part Two
def part_two(fileaddr):
    return










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
    
    # part_two_ans = part_two(fileaddr)
    # print(f"(Part 2) Solution: {part_two_ans}")
