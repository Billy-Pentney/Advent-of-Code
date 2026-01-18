
import numpy as np
# import regex as re
# from collections import defaultdict

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]
    disk_size = int(lines[0].strip())
    init_state = lines[1].strip()
    return disk_size, init_state

char_map = {'0':'1','1':'0'}

def make_reverse_inverse(text: str):
    rev_inv = ""
    for ch in reversed(text):
        rev_inv += char_map[ch]
    return rev_inv
    # rev_inv = text.replace("0", "2").replace("1","0").replace("2","1")
    # return str(reversed(rev_inv))

def make_dragon_string(init_data:str, min_length: int):
    data = init_data
    while len(data) < min_length:
        copy_data = make_reverse_inverse(data)
        data = data + "0" + copy_data
        print(f"Dragon curve: {len(data)}")
    return data

def calc_checksum(data: str):
    checksum = ""
    print(f"Find checksum of: {len(data)}")

    for i in range(0,len(data),2):
        ## Checkum gets 1 iff the pair is 00 or 11
        if data[i] == data[i+1]:
            checksum += "1"
        else:
            checksum += "0"

    ## Repeat if we got an even-length checksum
    if len(checksum) % 2 == 0:
        return calc_checksum(checksum)

    return checksum

def find_checksum(disk_size, init_state):
    expanded_data = make_dragon_string(init_state, disk_size)
    print(f"Got dragon string of length {len(expanded_data)}")
    full_disk = expanded_data[:disk_size]
    return calc_checksum(full_disk)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    disk_size, init_state = load(fname)
    print("Checksum:", find_checksum(disk_size, init_state))
