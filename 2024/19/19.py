
def load(fname):
    """
        Reads the problem input and parses it to the towels and designs.
    """

    with open(fname, "r") as file:
        towels = file.readline().strip("\n")
        file.readline()
        designs = file.readlines()
    
    towels = towels.split(", ")
    designs = [des.strip("\n") for des in designs]

    return towels, designs


def make_towel_dict(towels):
    """
        Constructs a dictionary of the towels, indexed by their first letter.
        This reduces the search time by providing a (faster) way to get the relevant towels for each design we check.
    """
    by_first_letter = {}
    for towel in towels:
        ltr = towel[0]
        if ltr not in by_first_letter.keys():
            by_first_letter[ltr] = []
        by_first_letter[ltr].append(towel)
    return by_first_letter



## Store the number of ways to construct each "sub-design".
memoization = {}

def count_ways(design, towels_dict, verbose=False, early_exit=True):
    """
        Recursively checks if the given design can be constructed from the collection of towels.
        If early_exit is true, then stop once we know the design is constructed.
        Returns the number of ways that the design can be constructed.
    """
    if len(design) == 0:
        ## End of the design
        return 1
    
    if design in memoization.keys():
        return memoization[design]

    if verbose:
        print(f"Checking {design}")
    
    memoization[design] = 0

    ltr = design[0]
    for towel in towels_dict.get(ltr, []):
        l = len(towel)
        if verbose:
            print(f"Checking \'{design}\' starts with \'{towel}\'")

        if design.startswith(towel):
            ## Recurse on the suffix of the design
            ways = count_ways(design[l:], towels_dict, verbose=verbose, early_exit=early_exit)
            memoization[design] += ways
            if early_exit and ways > 0:
                return ways
            ## Don't exit if we fail; there may be another towel which starts this design

    return memoization[design]



def part_one(towel_dict, designs, verbose=False):
    """
        Counts the number of designs that can be constructed from the given towels.
    """
    n_possible = 0
    memoization.clear()

    for i,design in enumerate(designs):
        # print(f"{i+1}/{len(designs)}")
        if count_ways(design, towel_dict, verbose=verbose, early_exit=True):
            n_possible += 1

    return n_possible


def part_two(towel_dict, designs, verbose=False):
    """
        Count the number of ways each design can be constructed from the towels and returns the sum.
    """

    n_ways = 0
    memoization.clear()

    for i,design in enumerate(designs):
        # print(f"{i+1}/{len(designs)}")
        ways = count_ways(design, towel_dict, verbose=verbose, early_exit=False)
        n_ways += ways

    return n_ways








from sys import argv


if __name__ == '__main__':
    fname = argv[1]
    towels, designs = load(fname)
    towel_dict = make_towel_dict(towels)
    print(towel_dict.items())

    n_possible = part_one(towel_dict, designs)
    print(f"(Part 1) Num Possible: {n_possible}")

    n_ways = part_two(towel_dict, designs, verbose=False)
    print(f"(Part 2) Num Ways: {n_ways}")