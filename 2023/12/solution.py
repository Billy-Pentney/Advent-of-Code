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
def split_line(line):
    match = re.match(line_regex, line)

    if match:
        line_symbols = match.group(1)
        counts = match.group(2)
        count_nums = [int(n) for n in counts.split(",") if len(n) > 0]
        return (rle_line(line_symbols), count_nums)

    return None


def split_lines(lines):
    splits = []
    for line in lines:
        split = split_line(line)
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


# # Recursively count the number of arrangements for a single line
# def arrangements_in_row(sequences, wanted_hashes, si=0, hi=0):
#     print(f"Run: {sequences} with expected_hashes {wanted_hashes}, si={si}, hi={hi}")
#     n = len(sequences)

#     while si < n-1 and sequences[si][1] == 0:
#         si+=1

#     # Run out of targets    
#     if (hi == len(wanted_hashes)):
#         # Must use '.' for rest of string (no '#' allowed)
#         for pair in sequences[si:]:
#             if pair[0] == '#':
#                 return 0
#         return 1
    
#     # Run out of sequences BUT targets is not empty
#     if si == n-1:
#         return 0  

#     # print(f"Run: {seqs_to_str(sequences)} with expected_hashes {wanted_hashes[hi:]}, si={si}, hi={hi}")
      
#     num_arranges = 0
#     req_len = wanted_hashes[hi]

#     seq = sequences[si]
#     next_seq = None

#     if si < n-1:
#         next_seq = sequences[si+1]

#     curr_char = seq[0]
#     curr_count = seq[1]

#     # If there are enough unknowns to add the first required count of '#'
#     if curr_char == '?':
#         if curr_count >= req_len:
#             # if we have enough unknowns to match the count
#             # and the next character can be a gap

#             # The index of the last '?' which can be set as '#' in a valid way
#             last_start = curr_count-req_len

#             num_blanks_req_after = 0

#             # Next sequence also has hashes, so we can't run to the end
#             if si < n-1 and next_seq[0] == '#':
#                 num_blanks_req_after = 1
            
#             last_start -= num_blanks_req_after

#             # Try each starting position in the empty space
#             #  [0, start-1] will be filled with '.'
#             #  [start, start+req_len] will be filled with '#'
#             #  [start+req_len+1, curr_count] will be filled with '.'
#             for start in range(0, last_start+1):
#                 # Insert req_len '#' symbols
#                 # j is the number of '.' inserted before the first '#'

#                 # The index of the last '#' inserted in this string
#                 hashes_end = start+req_len

#                 print(f" > Writing {req_len} # over [{start},{hashes_end}]")

#                 remaining_unknown = last_start+1 - hashes_end
#                 print("   Remaining ?:", remaining_unknown)

#                 # If the inserted '#' don't run to the end of the '?' string
#                 if remaining_unknown > 1:
#                     new_sequences = sequences.copy()
#                     # Reduce the number of '?' available for the next target
#                     new_sequences[si] = ['?', remaining_unknown-1]
#                     num_arranges += arrangements_in_row(new_sequences, wanted_hashes, si, hi+1)
#                 else:
#                     num_arranges += arrangements_in_row(sequences, wanted_hashes, si+1, hi+1)
    
#         elif si < n-1 and next_seq[0] == '#' and next_seq[1] < req_len:
#             next_hash_len = next_seq[1]
#             print("Merging with", next_seq)
            
#             for i in range(0, req_len - next_hash_len):
#                 new_sequences = sequences.copy()
#                 new_sequences[si] = ['#', i+1]
#                 if curr_count-i-1 > 0:
#                     new_sequences.insert(si, ['.', curr_count-i-1])
#                 num_arranges += arrangements_in_row(new_sequences, wanted_hashes, si, hi)
        
#         # Don't write any #, just fill with blanks
#         new_sequences = sequences.copy()
#         new_sequences[si] = ['.', curr_count]
#         num_arranges += arrangements_in_row(new_sequences, wanted_hashes, si+1, hi)

#     elif curr_char == '.':
#         # No hashes used
#         num_arranges += arrangements_in_row(sequences, wanted_hashes, si+1, hi)

#     elif curr_char == '#':
#         hashes_needed = wanted_hashes[hi] - curr_count

#         if hashes_needed == 0:
#             new_sequences = sequences.copy()
#             if si < n-1 and next_seq[0] == '?':
#                 # Cannot have consecutive hashes
#                 new_sequences[si+1] = ['.', next_seq[1]-hashes_needed]
#             num_arranges += arrangements_in_row(new_sequences, wanted_hashes, si+1, hi+1)

#         elif curr_count < wanted_hashes[hi] and si < n-1 and next_seq[0] == '?':
#             new_sequences = sequences.copy()
#             if (hashes_needed < next_seq[1]):
#                 new_sequences[si+1] = ['?', next_seq[1]-hashes_needed-1]
#                 num_arranges += arrangements_in_row(new_sequences, wanted_hashes, si+1, hi+1)
#             else:
#                 new_hashes = wanted_hashes.copy()
#                 new_hashes[hi] -= next_seq[1]
#                 num_arranges += arrangements_in_row(new_sequences, new_hashes, si+1, hi)

#     # print("Dead Branch")
#     return num_arranges

verbose = 0

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


def duplicate_list(l, k):
    l2 = l.copy()
    for i in range(k-1):
        l2.extend(l)
    return l2


def expand_each_row(splits, k):
    expanded_splits = [
        (duplicate_list(s,k), duplicate_list(c,k))
        for (s,c) in splits
    ]

    return expanded_splits



def sum_arrangements(fileaddr, part='1'):
    # lines = read_file(fileaddr)
    lines = ['??#???#?? 1,2,3']
            # #.##.###.
            # #.##..###
    splits = split_lines(lines)

    num_arranges = 0

    if part == '2':
        splits = expand_each_row(splits, 2)

    for i, split in enumerate(splits):
        line, counts = split
        arranges = greedy_arranges(line, counts, 0, 0)
        print(f"Arrangements of \"{seqs_to_str(line)}\" ({counts}): {arranges}")
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
    
