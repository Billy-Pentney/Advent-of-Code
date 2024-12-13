

from sys import argv
from os import mkdir
from os.path import exists

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

        fnames = [f'{dir_name}.py','test.txt','example.txt']
        for fname in fnames:
            with open(f'{dir_name}/{fname}', "w") as file:
                file.write("")
        
        print(f"Done {dir_name}!")