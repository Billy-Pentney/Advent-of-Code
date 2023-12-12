import os, sys

from distutils.dir_util import copy_tree

if __name__=='__main__':
    args = sys.argv[1:]
    daynum = args[0]

    if int(daynum) < 1 or int(daynum) > 31:
        print(f"Invalid day number #{daynum}")
    else:
        if (len(daynum) < 2):
            daynum = "0"+daynum

        source_dir = "./default"
        target_dir = f'./{daynum}/'

        if os.path.isdir(target_dir):
            print("Directory already exists!")
        else:
            os.mkdir(target_dir)
            print("Copying to target_dir:", target_dir)
            copy_tree(source_dir, target_dir)
