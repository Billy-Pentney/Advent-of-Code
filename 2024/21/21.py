
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        codes = [row.strip("\n") for row in file.readlines()]

    return np.array(codes)

UP = '^'
LEFT = '<'
RIGHT = '>'
DOWN = 'v'
ACC = 'A'



# Grid positions of each key, given as (row,column) 
numeric_positions = {
    '0': (1,0),
    'A': (2,0),
    '1': (0,1),
    '2': (1,1),
    '3': (2,1),
    '4': (0,2),
    '5': (1,2),
    '6': (2,2),
    '7': (0,3),
    '8': (1,3),
    '9': (2,3)
}

directional_positions = {
    LEFT: (0,0),
    DOWN: (1,0),
    RIGHT: (2,0),
    UP: (1,1),
    'A': (2,1)
}


numeric_keys = list(numeric_positions.keys())
directional_keys = list(directional_positions.keys())

numeric_moves = { key: {} for key in numeric_keys}
directional_moves = { key: {} for key in directional_keys }



def compute_min_steps():
    n_numeric_keys = len(numeric_keys)

    for i in range(n_numeric_keys):
        for j in range(n_numeric_keys):
            d1 = numeric_keys[i]
            d2 = numeric_keys[j]

            if i == j:
                numeric_moves[d1][d2] = []
                numeric_moves[d2][d1] = []
                continue

            p1 = numeric_positions[numeric_keys[i]]
            p2 = numeric_positions[numeric_keys[j]]

            p = [p1[0], p1[1]]
            t = [p2[0], p2[1]]

            sequence = []
            while p != t:
                # print(p,t)
                if p[0] > t[0] and p != [1,0]:           ## Cannot move left from 0 cell
                    ## Move left
                    sequence.append(LEFT)
                    p[0] -= 1
                elif p[0] < t[0]:
                    sequence.append(RIGHT)
                    p[0] += 1
                
                if p[1] > t[1] and p != [0,1]:           ## Cannot move down from 1 cell
                    sequence.append(DOWN)
                    p[1] -= 1
                elif p[1] < t[1]:
                    sequence.append(UP)
                    p[1] += 1

            # print(f"{d1} -> {d2}: {sequence}")
            numeric_moves[d1][d2] = sequence


    n_directional_keys = len(directional_keys)

    for i in range(n_directional_keys):
        for j in range(n_directional_keys):
            d1 = directional_keys[i]
            d2 = directional_keys[j]

            if i == j:
                directional_moves[d1][d2] = []
                continue

            p1 = directional_positions[d1]
            p2 = directional_positions[d2]

            p = [p1[0], p1[1]]
            t = [p2[0], p2[1]]

            sequence = []
            while p != t:
                if p[1] > t[1]:           
                    sequence.append(DOWN)
                    p[1] -= 1
                elif p[1] < t[1] and p != [0,0]:        ## Cannot move up from LEFT cell
                    sequence.append(UP)
                    p[1] += 1

                # print(p,t)
                if p[0] > t[0] and p != [1,1]:           ## Cannot move left from UP cell
                    ## Move left
                    sequence.append(LEFT)
                    p[0] -= 1
                elif p[0] < t[0]:
                    sequence.append(RIGHT)
                    p[0] += 1
                
                

            # print(f"{d1} -> {d2}: {sequence}")
            directional_moves[d1][d2] = sorted(sequence)




def find_numerical_instructions(code, start='A'):
    curr = start
    steps = []

    for dig in code:
        # print(f"{curr} -> {dig}")
        m = numeric_moves[curr][dig]
        steps.extend(m)
        steps.append('A')
        curr = dig

    return steps

def find_directional_instructions(code, start='A', verbose=True):
    curr = start
    steps = []

    for i,step in enumerate(code):
        m = directional_moves[curr][step]
        if step != curr:
            steps.extend(m)
        if verbose:
            print(f"{i}: {curr} -> {step} given by {m}")
            print('A')
        steps.append('A')
        curr = step

    return steps





def part_one(codes):
    for code in codes:
        r1_steps = find_numerical_instructions(code)
        r2_steps = find_directional_instructions(r1_steps, verbose=False)
        r3_steps = find_directional_instructions(r2_steps, verbose=True)
        print(code)
        print(f' 1: {"".join(r1_steps)}')
        print(f' 2: {"".join(r2_steps)}')
        print(f' 3: {"".join(r3_steps)}')
        print()



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    codes = load(fname)
    compute_min_steps()

    print(directional_moves.items())

    part_one(codes)