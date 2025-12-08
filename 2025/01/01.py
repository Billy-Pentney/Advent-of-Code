
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    instructions = []
    for row in lines:
        ## Indicate the sign
        sign = -1 if row[0] == 'L' else 1
        amount = int(row[1:])
        instructions.append(sign*amount)

    return instructions

def find_password(instructions, start=50, max_pos=99, method=1):
    position = start
    times_cross_zero = 0

    # print(position, times_cross_zero)
    for amount in instructions:
        new_position = (position + amount) 

        if method == 2:
            left_crosses = amount < 0 and abs(amount) >= position
            right_crosses = amount > 0 and abs(amount) >= max_pos - position

            if left_crosses or right_crosses:    
                times_cross_zero += abs(new_position) // (max_pos+1)
                
                if left_crosses and position > 0:
                    ## Add another if we cross zero on the first pass
                    times_cross_zero += 1
        
        new_position = new_position % (max_pos + 1)
        if method == 1 and new_position == 0:
            times_cross_zero += 1

        # print(position, amount, new_position, times_cross_zero)

        position = new_position

    return times_cross_zero




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    instructions = load(fname)
    password = find_password(instructions)
    print(f"Password Part 1: {password}")

    password2 = find_password(instructions, method=2)
    print(f"Password Part 2: {password2}")

