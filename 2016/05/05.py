
import numpy as np
from hashlib import md5



def find_password_advanced(door_id, use_position=False):
    """
    Solves Part 1 or Part 2 (parameter 'use_position' should be true for Part 2 solutions).

    Finds an 8-digit password incrementally, by searching for hashes which match the problem description.
    """
    

    print(f"Finding password for door: {door_id} (position={use_position})")
    password = list("________")
    ## Generate each digit
    index = 0

    for i in range(8):
        interesting = False
        ## Repeat until interesting
        while not interesting:
            inpt = door_id+str(index)
            h_hex = md5(inpt.encode()).hexdigest()
            if h_hex[:5] != '00000':
                index += 1
                continue

            if use_position:
                position = h_hex[5]
                ## Take the 7th digit
                new_digit = h_hex[6]
                if position in "1234567890":
                    pos = int(position)
                else:
                    pos = -1
            else:
                ## Take the 6th digit
                new_digit = h_hex[5]
                pos = i

            interesting = pos >= 0 and pos < len(password) and password[pos] == '_'
            if interesting:
                password[pos] = new_digit
                pw = "".join(password)
                print(f"{pos+1}/8: hash={h_hex[:6]}... {index}, {new_digit} -> {pw}")

            index += 1
            
    return "".join(password)







from sys import argv

if __name__ == '__main__':
    door_id = argv[1]

    password = find_password_advanced(door_id, use_position=False)
    print(f"Password 1: {password}")
    password_advanced = find_password_advanced(door_id, use_position=True)
    print(f"Password 2: {password_advanced}")