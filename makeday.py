
from os import mkdir, makedirs
from os.path import exists, join

from argparse import ArgumentParser

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



if __name__ == '__main__':

    arg_parser = ArgumentParser()
    arg_parser.add_argument('-year', type=int, help='Year of the challenge')
    arg_parser.add_argument('-days', type=int, nargs='+', help='Days to create')

    args = arg_parser.parse_args()

    year_num = str(args.year)
    year_dir = f'./{year_num}'

    if not exists(year_dir):
        mkdir(year_dir)

    for num in args.days:
        dir_name = str(num).zfill(2)
        day_dir = join(year_dir, dir_name)

        makedirs(day_dir, exist_ok=True)

        for fname in ['test.txt','example.txt']:
            with open(join(day_dir, fname), "w") as file:
                file.write("")

        py_name = f'{dir_name}.py'
        with open(join(day_dir, py_name), "w") as file:
            file.write(DEFAULT_PYTHON_SCRIPT)
        
        print(f"Created {year_num}-{dir_name}")

    print("Done!")