
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
        binary = list("0" * (len(btn)+1))
        for i in btn.strip("()").split(","):
            btn_num = int(i)
            if len(binary) <= btn_num:
                binary.extend('0'*(1+btn_num-len(binary)))
            binary[btn_num] = '1'
        ## Flip the order so the least significant button is on the right
        binary.reverse()
        button_binary = "".join(binary)
        button_val = int(button_binary, 2)
        # print(f"{btn} -> {button_val} ({button_binary})")
        button_lights.append(button_val)
    return button_lights


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
                'joltage_reqs': joltage_reqs
            }
            machines.append(machine)
            print(machine)

    return machines

def max_presses(goal, buttons, available_btn_idx, curr=0):
    if curr == goal:
        return 0
    
    if len(available_btn_idx) < 1:
        return 10000000000
        
    i = available_btn_idx[0]
    new_state = curr ^ buttons[i]
    ## Press the first button and try to solve with the rest
    presses_with_btn1 = 1 + max_presses(goal, buttons, available_btn_idx[1:], new_state)
    ## Don't press this button and try to solve with the rest
    presses_without_btn1 = max_presses(goal, buttons, available_btn_idx[1:], curr)

    return min(presses_with_btn1, presses_without_btn1)

def solve_machine(machine):
    buttons = machine["buttons"]
    goal = machine["goal"]

    ## We want to find the smallest subset of buttons which equals the goal.
    ## There's no point turning a button on and off again.

    available = range(len(buttons))
    return max_presses(goal, buttons, available, 0)


def find_total_presses_required(machines):
    total_presses = 0
    for i,m in enumerate(machines):
        presses = solve_machine(m)
        if presses < 10000000:
            total_presses += presses
        else:
            print(f"Machine {i}: {presses}")
        
    return total_presses



from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    machines = load(fname)
    # print(machines)

    part_one = find_total_presses_required(machines)
    print(f"Part 1: {part_one}")