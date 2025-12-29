
import numpy as np
from hashlib import md5
from time import process_time, sleep
# import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        text = [row.strip("\n") for row in file.readlines()]
    return text[0]

def find_tuplet(text, k):
    """
    Finds the index of the first contiguous sequence of (at least) k identical characters in the given string.
    e.g. find_tuplet("abcccd", 3) returns 2, while find_tuplet("")
    """
    for i in range(len(text)-k):
        if text[i:i+k] == text[i] * k:
            return i
    return None



def check_hash(hash, next_1000_hashes):
    ## Valid iff:
    # It contains three of the same character in a row, like 777. Only consider the first such triplet in a hash.
    # One of the next 1000 hashes in the stream contains that same character five times in a row, like 77777.

    triplet_start = find_tuplet(hash, 3)
    if triplet_start is None:
        return False
    
    triplet_char = hash[triplet_start]
    target = triplet_char * 5
    
    for next_hash in next_1000_hashes:
        if target in next_hash:
            # print(f"'{target}' in hash '{next_hash}'")
            return True
        
    return False

def hash_as_lower(text:str):
    return md5(text.encode()).hexdigest().lower()

## Store the result of hashing (this isn't used as the hashing algorithm has very few/no collisions)
# hash_cache = {}

def find_stretched_hash(text: str, num_repetitions: int):
    """
    Repeatedly applies the MD5 hash algorithm to a text, then to its hash, ... etc.
    """
    hashed = text

    for _ in range(num_repetitions):
        prev_hashed = hashed
        # hashed = hash_cache.get(hashed, )
        hashed = hash_as_lower(prev_hashed)        
        # hash_cache[prev_hashed] = hashed 

    return hashed


def find_otp(salt: str, key_index: int=64, hash_stretching: int=1):
    """
    Finds the specific index for the specified key, using the described OTP generation method.
    Note: this is slow for Part 2 but does produce a solution.

    Params:
        * salt: str - the initial salt, to which the index is appended.
        * key_index: int - the number of the key whose generation index is to be returned.
        * hash_stretching: int - (for part 2 only), the number of times to repeat the hashing process (default=1).
    """
    d = 1000

    hash_queue = ["" for i in range(d+1)]
    i = 0
    keys = []

    while len(keys) < key_index:
        inpt = (str(salt) + str(i)).lower()
        h = find_stretched_hash(inpt, hash_stretching)
        
        hash_queue[i%(d+1)] = h
        # print("hashes =", hash_queue)

        if i >= d:
            hi = (i-d) % (d+1)
            hash_to_check = hash_queue[hi]
            ## Select all other hashes around this one
            prev_hashes = hash_queue[hi+1:] + hash_queue[:hi]
            # print(f"Check {hash_to_check} in {hash_queue}, with {prev_hashes}")
            if check_hash(hash_to_check, prev_hashes):
                print(f"Key {len(keys)+1}: {i-d}")
                keys.append(i-d)

        i += 1

    return keys[-1]


## Sanity check: this solution re-calculates the next 1000 hashes, rather than using a circular queue

# def find_otp_brute(salt, key_index=64):
#     i = 0
#     keys = []

#     while len(keys) < key_index:
#         inpt = str(salt) + str(i)
#         h = hash_as_lower(inpt)
#         next_hashes = []
#         for j in range(i+1,i+1001):
#             next_hashes.append(hash_as_lower(str(salt)+str(j)))
#         if check_hash(h, next_hashes):
#             print(f"Key {len(keys)+1}: {i}")
#             keys.append(i)
        
#         i += 1

#     return keys[-1]





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    if len(argv) > 2:
        part = argv[2]
    else:
        part = '1'
    salt = load(fname)

    if part == '1':
        hash_stretching = 1
    elif part == '2':
        hash_stretching = 2017
    else:
        raise ValueError("Invalid value for 'Part'! Must be one of: '1', '2'")
    
    key_index = 64
    index_of_key = find_otp(salt, key_index, hash_stretching)
    print(f"Part {part}:", index_of_key)
