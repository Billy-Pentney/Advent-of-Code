import sys, os
import re


def read_file(fileaddr):
    strings = []
    with open(fileaddr, "r") as file:
        strings = [line.strip("\n") for line in file.readlines()]
    
    return strings



def is_nice(string):
    
    """ 
        Nice if all the following is true...
         * It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
         * It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
         * It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    """

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



def is_nice_revised(string):

    """
        Nice if all the following applies...

        * It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
        * It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.    
    """

    # Store the index of the first character in each first occurrence of a unique pair
    # e.g. for the string "abbcbbd", we finish with pair_ltrs = { 'ab':0, 'bb':1, 'bc':2, 'cb':3, 'bd':5 }
    pair_ltrs = {}

    ## True if we've seen a symmetric triplet, e.g. "xyx" or "aaa"
    sym_triple = None
    ## True if we've seen a pair twice, where the occurrences do not overlap
    pair_twice = None

    for i,ltr in enumerate(string):
        if not sym_triple and i > 1 and ltr == string[i-2]:
            ## Check for a triple of 'xyx' where x,y are any letter
            sym_triple = string[i-2:i+1]
        
        if not pair_twice and i > 0:
            pair = string[i-1:i+1]
            # print(pair)
            if pair in pair_ltrs.keys():
                ## If this pair does not overlap
                if pair_ltrs[pair] < i-2:
                    pair_twice = pair
            else:
                pair_ltrs[pair] = i-1

    # print()

    # print(pair_ltrs)
    nice = sym_triple is not None and pair_twice is not None
    # if sym_triple is not None:
    #     print(f" >> Triple: {sym_triple}")
    
    # if pair_twice is not None:
    #     print(f" >> Double-Pair: {pair_twice}")
    return nice




## Solve Part One
def count_nice(fileaddr, part=1, verbose=False):
    strings = read_file(fileaddr)

    n_nice = 0
    for s in strings:
        if part == 1:
            nice = is_nice(s)
        else:
            nice = is_nice_revised(s)

        if nice:
            n_nice += 1    
            if verbose:
                print(f"{s} >> NICE ({n_nice})")
        else:
            if verbose:
                print(f"{s} >> X")    

    return n_nice








if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    verbose = False

    part_one_ans = count_nice(fileaddr, 1, verbose=verbose)
    print(f"(Part 1) Solution: {part_one_ans}")
    
    part_two_ans = count_nice(fileaddr, 2, verbose=verbose)
    print(f"(Part 2) Solution: {part_two_ans}")
