import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


def parse_sequence(line):
    nums = line.replace("\n", "").split(" ")
    return [int(x) for x in nums]


def find_seq_of_diffs(sequence, rtl=False):
    diffs = []
    # Left-to-right
    if not rtl:
        for i in range(1, len(sequence)):
            diff = sequence[i] - sequence[i-1]
            diffs.append(diff)
    # Right-to-left
    else:
        for i in range(0, len(sequence)-1):
            diff = sequence[i] - sequence[i+1]
            diffs.append(diff)
       
    return diffs

def is_all_zeroes(sequence):
    for num in sequence:
        if num != 0:
            return False
    
    return True


def find_next_term(sequence):
    diff_seq = find_seq_of_diffs(sequence)

    # If the difference between consecutive terms is 0
    # Then, the entire sequence is the same
    if is_all_zeroes(diff_seq):
        return sequence[0]
    
    # Otherwise, add the next difference to the last term

    next_diff = find_next_term(diff_seq)
    return sequence[len(sequence)-1] + next_diff

def find_prev_term(sequence):
    # print(sequence)
    diff_seq = find_seq_of_diffs(sequence, rtl=True)

    # If the difference between consecutive terms is 0
    # Then, the entire sequence is the same
    if is_all_zeroes(diff_seq):
        return sequence[0]
    
    # Otherwise, add the next difference to the last term

    prev_diff = find_prev_term(diff_seq)
    return sequence[0] + prev_diff





## Solve Part One
def part_one(fileaddr):
    lines = read_file(fileaddr)
    sequences = [parse_sequence(line) for line in lines]
    next_terms = [find_next_term(seq) for seq in sequences]
    return sum(next_terms)


## Solve Part Two
def part_two(fileaddr):
    lines = read_file(fileaddr)
    sequences = [parse_sequence(line) for line in lines]
    prev_terms = [find_prev_term(seq) for seq in sequences]
    # print(prev_terms)
    return sum(prev_terms)










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
