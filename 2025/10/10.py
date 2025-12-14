
import numpy as np
import regex as re

machine_pattern = re.compile("\[([\.#]+)\] (\([\d,]+\)(?: \((?:\d|,)+\))*) (\{[\d,]+\})")

def parse_goal(goal: str):
    goal_num = goal.replace(".", "0").replace("#", "1")
    ## Flip the order, so the least significant light is on the right
    goal_num = goal_num[::-1]
    return int(f"0b{goal_num}", 2)

def parse_buttons(buttons: str):
    button_lights = []
    for btn in buttons.split(" "):
        binary = [0] * (len(btn)+1)
        for i in btn.strip("()").split(","):
            btn_num = int(i)
            if len(binary) <= btn_num:
                binary.extend([0]*(1+btn_num-len(binary)))
            binary[btn_num] = 1
        ## Flip the order so the least significant button is on the right
        binary.reverse()
        binary_string = "".join([str(b) for b in binary])
        binary_val = int(binary_string, 2)
        button_lights.append(binary_val)

    return button_lights

def parse_joltage(joltage: str):
    joltage_values = [int(x) for x in joltage.strip("\{\}").split(",")]
    return joltage_values



def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    machines = []
    for line in lines:
        match = machine_pattern.match(line)
        if match:
            goal = match.group(1)
            buttons = match.group(2)
            joltage_reqs = match.group(3)
            machine = {
                'goal': parse_goal(goal),
                'buttons': parse_buttons(buttons),
                'joltage': parse_joltage(joltage_reqs)
            }
            machines.append(machine)

    return machines

def find_max_presses_for_lights(goal, buttons, available_btn_idx, curr=0):
    if curr == goal:
        return 0
    
    if len(available_btn_idx) < 1:
        return 10000000000
        
    i = available_btn_idx[0]
    ## Logical XOR; each switch toggles the state.
    new_state = curr ^ buttons[i]
    ## Press the first button and try to solve with the rest
    presses_with_btn1 = 1 + find_max_presses_for_lights(goal, buttons, available_btn_idx[1:], new_state)
    ## Don't press this button and try to solve with the rest
    presses_without_btn1 = find_max_presses_for_lights(goal, buttons, available_btn_idx[1:], curr)

    return min(presses_with_btn1, presses_without_btn1)


def convert_decimal_to_base(num, base):
    coeffs = []
    while num > 0:
        coeffs.append(num % base)
        num = num // base
    coeffs.reverse()
    return np.array(coeffs)

def convert_base_to_decimal(coeffs, base):
    total = 0
    for coef in coeffs:
        total = total * base + coef
    return total


max_presses_cache = {}
verbose = True


def find_max_presses_for_joltage(buttons, available_btn_idx, curr, curr_presses=0, max_presses=None):
    """
    Recursively solves to find the minimum number of presses required to make the array curr equal to 0.
    :param: buttons - a list of the button arrays, each a list of the joltage indices they activate.
    :param: available_btn_idx - a list of the indices of the buttons which can be used.
    :param: curr - the current joltage array which needs to be set to 0.
    :param: curr_presses - the total number of button presses so far.
    :param: max_presses - the current best-known solution.
    """

    ## Exit if the goal is reached!
    if sum(curr) == 0:
        # print(" ============================================ DONE")
        return 0
    
    ## no solution if:
    ##  - there's no buttons left to press
    ##  - any joltage has exceeded the target
    ##  - we've found a solution but the current solution is more expensive
    if len(available_btn_idx) < 1 or min(curr) < 0 or (max_presses and curr_presses > max_presses):
        return None
        
    ## Use memoization of the solutions
    if tuple(curr) in max_presses_cache.keys():
        return max_presses_cache[tuple(curr)]
    
    ## Select the first button
    btn_idx = available_btn_idx[0]
    button_val = buttons[btn_idx]
    ## Find the joltage indices it contributes to
    button_nz_idx = np.nonzero(button_val)[0]

    ## Find how many times this button can be pressed without exceeding the joltage requirements
    max_times = curr * button_val
    max_times = max_times[np.where(button_val > 0)]

    if len(max_times) > 0 and min(max_times) > 0:
        times_can_press = min(max_times)
    else:
        times_can_press = 0

    ## If we already have a solution, then we have a limited number of moves we can make
    ## before any new solutions are more expensive.
    if max_presses is not None:
        ## Find how many moves we can make before matching the known best solution
        n_remaining_moves = max_presses - 1 - curr_presses 
        times_can_press = min(times_can_press, n_remaining_moves)

    ## Find for each button, the set of indices which are positive (i.e. the indices it turns on)
    buttons_nz_idx = [
        set(np.nonzero(buttons[z])[0])
        for z in available_btn_idx[1:]
    ]

    ## Start at the most presses and reduce the presses
    remainder = np.copy(curr) - times_can_press * button_val

    # Find the indices of the joltages which still need setting
    remainder_nz_idx = set(np.nonzero(remainder)[0])

    ## Store a list of candidate solutions, from which we select the minimum
    candidates = []
    ## Try every number of presses, including 0 (descending)
    for i in range(times_can_press,-1,-1):
        # new_available_btn_idx = available_btn_idx[1:]
        new_available_btn_idx = []
        ## Store the combined list of joltage indices covered by the remaining buttons
        new_coverage = set()

        ## Select the usable buttons for the next round by removing any which would add to a satisfied joltage level
        for j,z in enumerate(available_btn_idx[1:]):
            ## Check that all non-zero spaces for this button are in the remaining amount
            if len(set(buttons_nz_idx[j]).difference(remainder_nz_idx)) == 0:
                new_available_btn_idx.append(z)
                new_coverage = new_coverage.union(buttons_nz_idx[j])

        ## Check that the remaining buttons can set all indices in the remaining joltage
        if len(remainder_nz_idx.difference(new_coverage)) > 0:
            # print("Not solvable!")
            break

        if verbose:
            indent = " " * (len(buttons) - len(available_btn_idx))
            print(indent, curr, "-", str(i) + "*" + str(button_val), "=", remainder, f"(curr={curr_presses+i}, max={max_presses})")
        
        new_available_btn_idx = sorted(
            new_available_btn_idx, 
            key=lambda i: sum(curr * buttons[i]),
            reverse=True
        )

        ## Press the first button and then solve recursively
        num_presses = find_max_presses_for_joltage(buttons, new_available_btn_idx, remainder, curr_presses+i, max_presses)
        if num_presses is not None:
            ## If this met the joltage requirement, record the total moves
            candidates.append(num_presses + i)
            if max_presses is not None:
                max_presses = min(max_presses, curr_presses + num_presses + i)
            else:
                max_presses = curr_presses + num_presses + i
            break

        remainder += button_val
        ## Remove one press
        remainder_nz_idx = remainder_nz_idx.union(button_nz_idx)
    
    ## No solutions
    if len(candidates) == 0:
        return None
    
    max_presses_cache[tuple(curr)] = min(candidates)
    return max_presses_cache[tuple(curr)]



def find_total_presses_for_lights(machines):
    total_presses = 0
    for i,machine in enumerate(machines):
        buttons = machine["buttons"]
        goal = machine["goal"]

        ## We want to find the smallest subset of buttons which equals the goal.
        ## There's no point turning a button on and off again.

        available = range(len(buttons))
        presses = find_max_presses_for_lights(goal, buttons, available)

        if presses < 10000000:
            total_presses += presses
        else:
            print(f"Machine {i}: {presses}")
        
    return total_presses

def find_total_presses_for_joltage(machines):
    total_presses = 0
    for i,machine in enumerate(machines):
        print(f"Machine {i+1}: {machine}")

        ## Sort the buttons so we can eliminate them as we scan
        buttons = sorted(machine["buttons"], reverse=True)
        buttons_vals = ["{0:b}".format(button) for button in buttons]
        min_button_length = max([len(button) for button in buttons_vals])
        buttons_nums = [
            np.array([int(x) for x in reversed(list(button.rjust(min_button_length, "0")))])
            for button in buttons_vals
        ]
        joltage = np.array(machine["joltage"])
        
        ## (Heuristic) sort the remaining buttons by the amount of joltage values they contribute to
        available_btn_idx = sorted(
            range(len(buttons_nums)), 
            key=lambda i: tuple(joltage * buttons_nums[i]), 
            reverse=True
        )

        # We want to find the smallest subset of buttons which equals the joltage value        
        presses = find_max_presses_for_joltage(buttons_nums, available_btn_idx, joltage)
        
        print(f" > Presses = {presses}")
        if presses:
            total_presses += presses
        
    return total_presses



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    machines = load(fname)
    # print(machines)

    # part_one = find_total_presses_for_lights(machines)
    # print(f"Part 1: {part_one}")

    part_two = find_total_presses_for_joltage(machines)
    print(f"Part 2: {part_two}")


