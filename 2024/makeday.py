

from sys import argv
from os import mkdir
from os.path import exists

DEFAULT_PYTHON_SCRIPT = \
"""
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        grid = [list(row.strip("\\n")) for row in file.readlines()]

    return np.array(grid)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]
"""



if __name__=='__main__':

    if len(argv) < 2:
        print("No argument supplied")
        exit(1)

    for arg in argv[1:]:
        try:
            num = int(arg)
        except ValueError:
            print(f"Cannot convert {arg} to num")
            continue

        dir_name = str(num).zfill(2)

        if not exists(dir_name):
            mkdir(dir_name)

        fnames = ['test.txt','example.txt']
        for fname in fnames:
            with open(f'{dir_name}/{fname}', "w") as file:
                file.write("")


        py_name = f'{dir_name}.py'
        with open(f"{dir_name}/{py_name}", "w") as file:
            file.write(DEFAULT_PYTHON_SCRIPT)
        
        print(f"Done {dir_name}!")