
import numpy as np


def load(fname):
    with open(fname, "r") as file:
        lines = file.readlines()

    page_orders = []
    updates = []

    all_orders_seen = False
    for line in lines:
        line = line.strip("\n")
        if len(line) == 0:
            all_orders_seen = True
        elif all_orders_seen:
            pages = [int(x) for x in line.split(",")]
            updates.append(pages)
        else:
            pages = [int(x) for x in line.split("|")]
            page_orders.append(pages)
    
    return page_orders, updates


def build_dependency_dict(orders):
    """
        Returns a dictionary from each page to the list of its dependencies.
        E.g. dep[X] = [A,B,Y] means that pages A,B,Y are required by page X.
    """
    dep = {}
    for req, next in orders:
        if next not in dep.keys():
            dep[next] = []
        dep[next].append(req)
    return dep


def find_valid_updates(deps, updates):

    update_validity = np.full(len(updates), False)

    for i,update in enumerate(updates):
        printed = []
        is_valid = True
        for p in update:
            printed.append(p)
            reqs = set(deps.get(p, []))
            # Requirements which appear in the update
            reqs = reqs.intersection(update)
            # Check if all requirements have been printed
            n_missing = sum([1 for req in reqs if req not in printed])
            if n_missing > 0:
                is_valid = False
                break

        update_validity[i] = is_valid
    
    return update_validity


def compute_sum_of_centres(updates, verbose=False):
    sum_centre_nums = 0
    for update in updates:
        if verbose:
            print(f" * {update}")
        mid_idx = len(update)//2
        mid_num = update[mid_idx]
        sum_centre_nums += mid_num
    return sum_centre_nums


def part_one(orders, updates):
    deps = build_dependency_dict(orders)
    validity = find_valid_updates(deps, updates)
    valid_updates = np.array(updates, dtype='object')[validity]

    sum_centre_nums = compute_sum_of_centres(valid_updates)
    return sum_centre_nums



def fix_updates(deps, updates):
    corrected_updates = []
    for update in updates:
        # For each page, get the requirements from the update
        reqs = {
            p:set(deps.get(p, [])).intersection(update) 
            for p in update
        }

        ## Compute the "successors"
        succs = {p:[] for p in update}
        for p,p_reqs in reqs.items():
            for q in p_reqs:
                succs[q].append(p)

        ## Get the pages which have no requirements
        queue = [p for p in update if len(reqs[p]) == 0]

        ## BFS from the end point
        fixed = []
        while len(queue) > 0:
            curr = queue[0]
            queue = queue[1:]
            fixed.append(curr)

            ## Consider each node which requires curr
            for succ in succs[curr]:
                # Remove this dependency
                reqs[succ].remove(curr)
                # If the successor has no other incoming edges, add it to the ordering
                if len(reqs[succ]) == 0:
                    queue.append(succ)

        corrected_updates.append(fixed)
        # print(f"Corrected {update} to {fixed}")

    return corrected_updates


def part_two(orders, updates):
    deps = build_dependency_dict(orders)
    validity = find_valid_updates(deps, updates)
    # Get the IN-valid updates
    invalid_updates = np.array(updates, dtype='object')[~validity]

    corrected_updates = fix_updates(deps, invalid_updates)
    return compute_sum_of_centres(corrected_updates)









from sys import argv

if __name__ == '__main__':

    fname = argv[1]

    page_orders, updates = load(fname)

    sum_part_one = part_one(page_orders, updates)
    print(f"(Part 1) Sum of Valid Update Centres: {sum_part_one}")

    sum_part_two = part_two(page_orders, updates)
    print(f"(Part 2) Sum of corrected invalid orders: {sum_part_two}")

    # print(f"Orders: {page_orders}")
    # print(f"Updates: {updates}")