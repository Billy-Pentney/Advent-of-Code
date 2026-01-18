
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        commands = [list(row.strip("\n")) for row in file.readlines()]
    return commands


pad_1 = np.array([
    ['1','2','3'],
    ['4','5','6'],
    ['7','8','9']
])
pad_2 = np.array([
    ['#','#','1','#','#'],
    ['#','2','3','4','#'],
    ['5','6','7','8','9'],
    ['#','A','B','C','#'],
    ['#','#','D','#','#']
])

def find_code(commands, pad, start_x, start_y):
    code = []
    x,y = start_x, start_y
    n_rows = pad.shape[0]
    n_cols = pad.shape[1]

    for command in commands:
        # print("New command")
        for step in command:
            # print(step, x,y)
            if step == 'U' and y > 0 and pad[y-1,x] != '#':
                y -= 1 
            elif step == 'D' and y < n_rows-1 and pad[y+1,x] != '#':
                y += 1
            elif step == 'L' and x > 0 and pad[y,x-1] != '#':
                x -= 1
            elif step == 'R' and x < n_cols-1 and pad[y,x+1] != '#':
                x += 1

        digit = pad[y, x]
        code.append(str(digit))

    return "".join(code)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    commands = load(fname)

    code_part_one = find_code(commands, pad_1, start_x=1, start_y=1)
    print(f"Part one: {code_part_one}")
    code_part_two = find_code(commands, pad_2, start_x=0, start_y=2)
    print(f"Part two: {code_part_two}")
