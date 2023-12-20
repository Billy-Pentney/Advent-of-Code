import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    rulelines = lines[:-1]
    input = lines[-1].replace("\n", "")

    # Construct the mapping of each element to a list of its replacements
    rules = {}
    for line in rulelines:
        match = re.match(pattern, line)
        if match:
            from_elem = match.group(1)
            to_elem = match.group(2)
            if from_elem in rules.keys():
                rules[from_elem].append(to_elem)
            else:
                rules[from_elem] = [to_elem]

    return rules, input




pattern = "(\w+) => (\w+)"


def find_new_compounds(input, rules, i, j):
    compounds = set()
    if i < j:
        elem_to_match = input[i:j+1]
    else:
        elem_to_match = input[i]

    if elem_to_match in rules.keys():
        for res in rules[elem_to_match]:
            new_compound = ""
            if i > 0:
                new_compound = input[0:i]
            new_compound += res
            if i < len(input):
                new_compound += input[j+1:]
            compounds.add(new_compound)

    print(f"Replacing {i},{j} produces {compounds}")
    return compounds



## Solve Part One
def part_one(fileaddr):
    rules, input = read_file(fileaddr)
    print(rules)

    all_compounds = set()
    for i in range(len(input)):
        if i > 0:
            all_compounds = all_compounds.union(find_new_compounds(input, rules, i-1, i))
        all_compounds = all_compounds.union(find_new_compounds(input, rules, i, i))

    return len(all_compounds)


reduction_target = "e"
min_steps = { reduction_target: 0 }


def reduce_to(input: str, rules):
    if input == reduction_target:
        return 0
    
    # print(f"From {input} to {reduction_target}")

    min_steps[input] = None
    
    max_len = 0
    all_repls = []
    # Find all rules whose RHS is in the input 
    for key, repls in rules.items():
        for repl in repls:
            if repl in input:
                all_repls.append((repl, key))
                if len(repl) > max_len:
                    max_len = len(repl)

    # Sort by descending replacement length
    all_repls = sorted(all_repls, key=lambda r: len(r[0]), reverse=True)

    max_len_repls = [r for r in all_repls if len(r[0]) == max_len]

    # print(f" >> Found {len(max_repls)} applicable rule(s)!")
    # Try all suitable replacements recursively
    for repl, key in max_len_repls:
        # print(f" >> Apply: {repl} -> {key}")
        new_input = input.replace(repl, key, 1)

        if new_input in min_steps.keys():
            steps_req = min_steps[new_input]
        else:
            steps_req = reduce_to(new_input, rules)

        if steps_req is None:
            # Cannot reach target from this state
            continue
        else:
            # Include this replacement step
            steps_req += 1

        if min_steps[input] is None or steps_req < min_steps[input]:
            min_steps[input] = steps_req

    if min_steps[input] is None:
        # print("Last Resort!")
        other_repls = [r for r in all_repls if len(r[0]) < max_len]
        for repl, key in other_repls:
            # print(f" >> Apply: {repl} -> {key}")
            new_input = input.replace(repl, key)

            if new_input in min_steps.keys():
                steps_req = min_steps[new_input]
            else:
                steps_req = reduce_to(new_input, rules)

            if steps_req is None:
                # Cannot reach target from this state
                continue
            else:
                # Include this replacement step
                steps_req += 1

            if min_steps[input] is None or steps_req < min_steps[input]:
                min_steps[input] = steps_req
    #     print(f"Cannot reduce {input} to {reduction_target}")

    return min_steps[input]


## Solve Part Two
def part_two(fileaddr):
    rules, input = read_file(fileaddr)

    # Remove rules which can't be applied as they don't appear in the RHS
    # removed = 0
    # for key, repls in rules.items():
    #     new_repls = [repl for repl in repls if repl in input]
    #     rules[key] = new_repls
    #     removed += len(repls) - len(new_repls)
    # print(f"Removed {removed} unused rules!")

    reduce_to(input, rules)
    return min_steps[input]










if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if os.path.exists(fileaddr):
        if (part == '1'):
            result = part_one(fileaddr)
        else:
            result = part_two(fileaddr)
        print("Result:",result)
    else:
        print(f"Could not find file at location {fileaddr}")
    
