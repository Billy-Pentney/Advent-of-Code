
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        banks = [row.strip("\n") for row in file.readlines()]

    return banks


cache_max_joltage = {}

def find_max_joltage(bank: str, n_to_select: int) -> str:
    """
    Recursively solves to find the optimum selection of n batteries from the bank.

    Param
    ----
    * bank: a string of digits, where each one corresponds to a battery of that power.
    * n_to_select: the number of batteries we can choose

    Returns
    ----
    A string with the value of the maximum-joltage selection.
    """

    if len(bank) == n_to_select:
        return bank
    
    ## Check if it's possible
    if len(bank) == 0 or len(bank) < n_to_select or n_to_select < 1:
        return ""
    
    ## Encode each case based on both the available batteries and the num we can choose
    code = f"{bank}/{n_to_select}"
    if code in cache_max_joltage.keys():
        return cache_max_joltage[code]

    ## Consider two cases: with and without the first battery

    head, tail = bank[0], bank[1:]
    ## Find the maximum joltage *including* this battery
    max_with = head + find_max_joltage(tail, n_to_select-1) 
    ## Find the maximum joltage *excluding* this battery
    max_without = find_max_joltage(tail, n_to_select)

    ## Convert the solutions to integers
    joltage_with = int(max_with)
    joltage_without = int(max_without)

    ## Choose the case that maximises the joltage
    if joltage_with > joltage_without:
        max_joltage = max_with
    else:
        max_joltage = max_without

    ## Cache the result to speed-up future runs
    cache_max_joltage[code] = max_joltage
    return max_joltage




def compute_total_joltage(banks, part=1):
    """
    Calculates the total max joltage for the given power banks, by summing.
    Parameter 'part' indicates which part of the question (1 or 2)
    """
    n_to_select = 2 if part == 1 else 12
    cache_max_joltage.clear()
    return sum([
        int(find_max_joltage(bank, n_to_select)) 
        for bank in banks
    ])





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    banks = load(fname)

    joltage_part_one = compute_total_joltage(banks, part=1)
    print("Part 1:", joltage_part_one)
    
    joltage_part_two = compute_total_joltage(banks, part=2)
    print("Part 2:", joltage_part_two)