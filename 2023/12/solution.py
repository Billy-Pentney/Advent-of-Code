import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()
    return lines


# Apply run-length-encoding to the line of symbols
#   e.g. ".??.###?." -> [('.',1),('?',2),('.',1),('#',3),('?',1),('.',1)]
def rle_line(line):
    stack = []

    for char in line:
        n = len(stack)
        if n == 0 or stack[n-1][0] != char:
            # New or different Character
            stack.append([char, 1])
        else:
            # Increment count of last character on the stack
            stack[n-1][1] += 1

    return stack

line_regex = "([#?.]+) (\d+(?:,\d+)*)"
# Convert a line to its string of symbols ('#','?','.') and list of counts
def split_line(line, apply_rle):
    match = re.match(line_regex, line)

    if match:
        line_symbols = match.group(1)
        counts = match.group(2)
        count_nums = [int(n) for n in counts.split(",") if len(n) > 0]
        if apply_rle:
            return (rle_line(line_symbols), count_nums)
        else:
            return line_symbols, count_nums

    return None


def split_lines(lines, apply_rle=True):
    splits = []
    for line in lines:
        split = split_line(line, apply_rle)
        if split is not None:
            splits.append(split)

    # print(splits)
    return splits


def seqs_to_str(sequences, si=-1):
    s = ""
    for i, seq in enumerate(sequences):
        if i == si:
            s += "|"
        s += seq[0]*seq[1]
    return s 


verbose = 0


def arrangements_three(line, counts, i=0, num_hash = 0, count_i = 0):
    print("     " + "".join(line[:i])+"|"+"".join(line[i+1:]))

    arranges = 0
     
    if i == len(line)-1:
        if count_i == len(counts)-1:
            return 1
        elif counts[count_i] == num_hash and len(counts) == 1:
            return 1

        return 0

    char = line[i]

    # No more counts required
    if count_i == len(counts)-1:
        # Any more hashes would be seen in counts
        if char == '#':
            return 0
        arranges = arrangements_three(line, counts, i+1, num_hash=0, count_i=count_i)       
         
    elif char == '.':
        # Reset the hash number
        if num_hash > 0 and num_hash != counts[count_i]:
            return 0
        arranges = arrangements_three(line, counts, i+1, num_hash=0, count_i=count_i+1) 

    elif char == '#':
        # Too many '#'s consecutively
        if num_hash >= counts[count_i]:
            return 0
        arranges = arrangements_three(line, counts, i+1, num_hash=num_hash+1, count_i=count_i)

    else:
        # Have a '?'

        if num_hash > 0:
            if num_hash < counts[count_i]:
                # Need to increase consecutive count of '#'
                line[i] = '#'
                arranges = arrangements_three(line, counts, i+1, num_hash=num_hash+1, count_i=count_i)
            elif num_hash == counts[count_i]:
                # Have the exact count of '#'; need to end block with '.'
                line[i] = '.'
                arranges = arrangements_three(line, counts, i+1, num_hash=0, count_i=count_i+1)
            else:
                # Too many consecutive hashes, so fail
                return 0
        else:
            # Bifurcation

            # Treat ? as '.'
            line[i] = '.'
            arranges += arrangements_three(line, counts, i+1, num_hash=0, count_i=count_i)

            # Treat ? as '#'
            line[i] = '#'
            arranges += arrangements_three(line, counts, i+1, num_hash=num_hash+1, count_i=count_i)
    
    return arranges



def greedy_arranges(seqs, counts, count_hash=0, si=0):
    arranges = 0
    
    while len(seqs)-1 > si and seqs[si][1] == 0:
        si+=1

    indent = si*" "

    if verbose == 1:
        print(f"{indent}Running on {seqs_to_str(seqs, si)}, with counts {counts}, and #_count={count_hash}")        

    if len(counts) == 0 or (len(counts) == 1 and counts[0] == count_hash):
        # print("empty counts!")
        # Only 1 combination for rest of string (no '#' allowed)
        for pair in seqs[si:]:
            if pair[0] == '#':
                return 0
        if verbose == 1:
            print("Solution found!")
        return 1

    if len(seqs) == si:
        # print("empty seqs!")
        # No valid arrangements since counts <> []
        return 0
    
    seq = seqs[si]

    if seq[0] == '#':
        count_hash = count_hash + seq[1]

        if count_hash > counts[0]:
            # Too many #s which do not match the expected count
            return arranges
        else:
            return greedy_arranges(seqs, counts, count_hash, si+1)

    elif seq[0] == '.':
        if count_hash == 0:
            arranges += greedy_arranges(seqs, counts, 0, si+1)
        elif counts[0] == count_hash:
            arranges += greedy_arranges(seqs, counts[1:], 0, si+1)

    elif seq[0] == '?':
        # Hashes in the previous sequence, so we must match to the current count
        if count_hash > 0:
            hashes_needed = counts[0] - count_hash                
            hash_first_seqs = seqs.copy()

            if hashes_needed >= seq[1]:
                # Make all the '?' into '#'
                hash_first_seqs[si] = ['#', seq[1]]
                count_hash += seq[1]
                arranges += greedy_arranges(hash_first_seqs, counts, count_hash, si+1)

            else:
                # Only need the first few of hash


                if hashes_needed == 0:
                    # need a dot
                    counts = counts[1:]
                    hash_first_seqs[si] = ['.', 1]
                    hash_first_seqs.insert(si+1, ['?', seq[1]-1])
                    count_hash = 0

                else:
                    hash_first_seqs[si] = ['#', hashes_needed]
                    # Number of ?s which are not set in this assignment
                    unused = seq[1] - hashes_needed
                    if (unused > 0):
                        hash_first_seqs.insert(si+1, ['?', unused])
                    count_hash += hashes_needed

                arranges += greedy_arranges(hash_first_seqs, counts, count_hash, si+1)
        
        else:
            # Otherwise, the previous character was a '.', so consider both cases
            h = min(seq[1], counts[0])
            # make the first h ?s into '#'
            new_seqs = seqs.copy()
            new_seqs[si] = ['#', h]
            if (h < seq[1]):
                new_seqs.insert(si+1,['?', seq[1]-h])
            arranges += greedy_arranges(new_seqs, counts, h, si+1)

            dot_first_seqs = seqs.copy()
            dot_first_seqs[si] = ['.', 1]
            if (seq[1] > 0):
                dot_first_seqs.insert(si+1, ['?', seq[1]-1])
            arranges += greedy_arranges(dot_first_seqs, counts, 0, si+1)

    # print(f"Branch produced {arranges} arrangements")
    return arranges


def duplicate_list(l, k, merge_at_boundary=False):
    l2 = l.copy()
    print(l2)
    for i in range(k-1):
        l_cpy = l.copy()
        if merge_at_boundary and l2[len(l2)-1][0] == l_cpy[0][0]:
            l2[len(l2)-1][1] += l_cpy[0][1]
            l2.extend(l_cpy[1:])
        else:
            l2.extend(l_cpy)
    return l2


def expand_each_row(splits, k):
    expanded_splits = [(duplicate_list(s, k, True), duplicate_list(c, k)) for s,c in splits]
    return expanded_splits


def sum_arrangements(fileaddr, part='1'):
    lines = read_file(fileaddr)
    # lines = ['??#???#?? 1,2,3']
            # #.##.###.
            # #.##..###
    splits = split_lines(lines, apply_rle=False)

    num_arranges = 0

    # if part == '2':
    #     splits = expand_each_row(splits, 2)
        # print(splits)

    for i, split in enumerate(splits):
        line, counts = split
        # print(line)
        arranges = arrangements_three(list(line), counts)
        print(f"Arrangements of \"{line}\" ({counts}): {arranges}")
        num_arranges += arranges

    return num_arranges










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        result = sum_arrangements(fileaddr, part)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
