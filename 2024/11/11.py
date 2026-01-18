
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        stones = [int(x) for x in file.readline().strip("\n").split(" ")]

    ## Use 64-bit because the multiplication might get large!!
    return stones



def count_stones(stones, n_rounds=25):

    ## The stone-list has a lot of redundancy and all stones with the same value have the same operation applied.
    ## Therefore, we can group the stones by their value and perform the rules in groups.

    stone_counts = {}
    for stone in stones:
        stone_counts[stone] = stone_counts.get(stone,0)+1

    for r in range(n_rounds):
        ## Make a new count-dictionary for *after* this round
        new_cnts = {}

        for stone, cnt in stone_counts.items():
            if stone == 0:
                new_cnts[1] = new_cnts.get(1,0) + cnt 
            elif stone == 1:
                new_cnts[2024] = new_cnts.get(2024,0) + cnt
            else:
                stone_str = str(stone)
                l = len(stone_str)
                if l % 2 == 0:
                    left = int(stone_str[:l//2])
                    right = int(stone_str[l//2:])
                    
                    new_cnts[left] = new_cnts.get(left, 0)+cnt
                    new_cnts[right] = new_cnts.get(right, 0)+cnt
                else:
                    new_stone = stone*2024
                    new_cnts[new_stone] = new_cnts.get(new_stone, 0)+cnt
             
        stone_counts = new_cnts
    
    n_stones = sum(stone_counts.values())
    return n_stones





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    stones = load(fname)
    print(stones)

    n_stones_25 = count_stones(stones, 25)
    print(f"(Part 1) Num stones after 25 steps: {n_stones_25}")

    n_stones_75 = count_stones(stones, 75)
    print(f"(Part 2) Num stones after 75 steps: {n_stones_75}")
