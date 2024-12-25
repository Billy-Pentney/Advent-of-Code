

def load_file(fname):
    levels = []

    with open(fname, "r") as file:
        lines = file.readlines()
        for line in lines:
            nums = [int(x) for x in line.split(" ")]
            levels.append(nums)

    return levels



def is_increasing(diffs):
    n_inc = 0
    for diff in diffs:
        if diff > 0:
            n_inc += 1
    return n_inc >= len(diffs)//2 



def is_unsafe(report):
    diffs = [report[i]-report[i-1] for i in range(1,len(report))]
    all_increasing = is_increasing(diffs)

    bad_at = []
    for i,diff in enumerate(diffs):
        diff_inc = diff > 0
        if abs(diff) < 1 or abs(diff) > 3 or (diff_inc and not all_increasing) or (not diff_inc and all_increasing):
            bad_at.append(i)

    return bad_at
            



def part_one(reports, allow_bad=False):

    """
        Rules:
            1. The levels are either all increasing or all decreasing.
            2. Any two adjacent levels differ by at least one and at most three.

    """

    safe = []
    for report in reports:
        bad_at = is_unsafe(report)

        # print(report)
        # print(bad_at)

        if len(bad_at) == 0:
            safe.append(report)
            # print(f"SAFE: {report}")

        elif allow_bad:
            is_safe = False

            ## Check each bad index
            for bad in bad_at:
                for drop_idx in [bad, bad+1]:
                    ## Form the string, excluding this level
                    dropped = report[:drop_idx] + report[drop_idx+1:]
                    if len(is_unsafe(dropped)) == 0:
                        is_safe = True
                        break
                if is_safe:
                    break
            if is_safe:
                safe.append(report)

    # print("\n"+"-"*10 + "SAFE" + "-"*10)
    # for rep in safe:
    #     print(rep)
    return len(safe)




import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("No filename!")
        exit(1)

    fname = sys.argv[1]
    reports = load_file(fname)
    # print(reports)

    print(f"(Part 1) Total safe: {part_one(reports, allow_bad=False)}")    
    print(f"(Part 2) Total safe: {part_one(reports, allow_bad=True)}")