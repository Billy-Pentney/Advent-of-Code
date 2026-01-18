
import numpy as np
# import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        lines = [tuple(row.strip("\n").split(" ")) for row in file.readlines()]

    return lines

def play_round(other_idx, self_idx):
    if (other_idx + 1) % 3 == self_idx:
        ## Other = Rock, self = Paper
        return 1
    elif (self_idx + 1) % 3 == other_idx:
        ## Self = rock, Other = Paper
        return -1
    ## Tie
    return 0
    
def count_total_score(lines):
    total_score = 0
    for other, me in lines:    
        other_idx = "ABC".index(other)
        me_idx = "XYZ".index(me)
        result = play_round(other_idx, me_idx)
        score = (me_idx+1) + 3 * (result+1)
        total_score += score

    return total_score


def count_total_score_part_two(lines):
    total_score = 0
    for other, me in lines:    
        other_idx = "ABC".index(other)
        result_idx = "XYZ".index(me)
        if result_idx == 0:
            ## Need to lose
            me_idx = (other_idx+2)%3
        elif result_idx == 1:
            ## Need to draw
            me_idx = other_idx
        else:
            me_idx = (other_idx+1)%3

        result = play_round(other_idx, me_idx)
        score = (me_idx+1) + 3 * (result+1)
        total_score += score

    return total_score



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    lines = load(fname)
    part_one = count_total_score(lines)
    print("Part one:", part_one)
    part_two = count_total_score_part_two(lines)
    print("Part two:", part_two)