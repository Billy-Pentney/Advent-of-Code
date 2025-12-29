
import regex as re

disc_pattern = r"Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)\."

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    disc_pos = []
    disc_widths = []
    for line in lines:
        match = re.match(disc_pattern, line)
        if match:
            # disc_num = int(match.group(1))            ## Not used
            num_positions = int(match.group(2))
            # init_time = int(match.group(3))           ## Always 0
            init_pos = int(match.group(4))
            disc_pos.append(init_pos)
            disc_widths.append(num_positions)

    return disc_pos, disc_widths

def check_drop(disc_pos, widths):
    """ Returns true if dropping a capsule with the current disc positions would lead to it
        falling through all of them. This is equivalent to checking that for all discs i, after i time-steps, 
        disc i reaches position k (the same for all discs).
    """
    last_pos = None
    for i, pos in enumerate(disc_pos):
        new_pos = (pos+i) % widths[i]
        ## Check that this disc is in the same position as the previous disc
        if i > 0 and new_pos != last_pos:
            return False
        last_pos = new_pos
    return True


def find_alignment(disc_pos: list, disc_widths: list):
    """
    Finds the time step at which all the discs will be aligned.
    """
    solved = False
    ## We want discs to be a sequence: t,t+1,t+2,t+3,...t+D
    t = 0

    print_step = 50000

    while not solved:
        if t % print_step == 0:
            print(f"At t={t}, {disc_pos}")

        ## Increment each disc's position
        disc_pos = [(pos + 1) % width for pos,width in zip(disc_pos, disc_widths)]

        solved = check_drop(disc_pos, disc_widths)
        if not solved:
            t += 1
        else:
            print(f"Solved! {disc_pos}")

    return t



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    disc_pos, disc_widths = load(fname)
    solution = find_alignment(disc_pos, disc_widths)
    print("Drop time:", solution)

