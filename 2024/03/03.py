
import regex as re

reg_mult = re.compile("mul\((\d+),(\d+)\)")

reg_do_dont = re.compile("((do)|(don\'t))\(\)")

def read_file(fname):
    with open(fname, "r") as file:
        code = file.read()
    return code.strip("\n")


def part_one(code, verbose=False):
    matches = reg_mult.findall(code)
    mults = [(int(m[0]),int(m[1])) for m in matches]
    if verbose:
        print([f"{x}*{y}" for x,y in mults])
    evals = [x*y for x,y in mults]
    return sum(evals)


def part_two(code):
    matches = reg_do_dont.finditer(code)
    curr = 0
    skip_next = False
    totals = []

    for match in matches:
        keyword = match.group(0)

        section = code[curr:match.start()]
        # print(f"{skip_next} from {curr} to {keyword}")

        if not skip_next:
            ## Not skipped last segment
            # sections.append(section)
            section_total = part_one(section, verbose=False)
            totals.append(section_total)
            print(f" * Do: \"{section}\" with total {section_total}")
        else:
            print(f" * Don't: \"{section}\"")

        # print(" " * 30)

        skip_next = len(keyword) == 7
        curr = match.end()

    ## Add the final section after the last 'do'
    if curr < len(code) and not skip_next:
        section = code[curr:] 
        section_total = part_one(section, verbose=False)
        print(f" * Do: \"{section}\" with total {section_total}")
        totals.append(section_total)

    return sum(totals)



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    code = read_file(fname)
    total = part_one(code)
    print(f"(Part 1) Total = {total}")

    total_part_two = part_two(code)
    print(f"(Part 2) Total = {total_part_two}")


