
import numpy as np
import regex as re
from collections import defaultdict

re_val_to_bot = r"value (\d+) goes to bot (\d+)"
## 1 - value
## 2 - bot number

re_bot_to_output = r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)"
## 1 - bot number
## 2 - low bot/target
## 3 - low bot number or low target number
## 4 - high bot/target
## 5 - high bot number or high target number

from abc import ABC
from typing import List

class Expression(ABC):
    def __init__(self):
        pass

class Assignment(Expression):
    def __init__(self, value_num, bot_num):
        self.value_num = value_num
        self.bot_num = bot_num

class Comparison(Expression):
    def __init__(self, bot_num: int, low_target: str, low_target_num: int, high_target: str, high_target_num: int):
        self.bot_num = bot_num
        self.low_is_bot = low_target == 'bot'
        self.low_target_num = low_target_num
        self.high_is_bot = high_target == 'bot'
        self.high_target_num = high_target_num

class BotOutputs():
    def __init__(self, low_is_bot: str, low_num: int, high_is_bot: str, high_num: int):
        self.low_is_bot = low_is_bot
        self.low_num = low_num
        self.high_is_bot = high_is_bot
        self.high_num = high_num

def load(fname):
    with open(fname, "r") as file:
        lines = [row.strip("\n") for row in file.readlines()]

    expressions = []
    for line in lines:
        match = re.match(re_val_to_bot, line)
        if match:
            value_num = int(match.group(1))
            bot_num = int(match.group(2))
            expressions.append(Assignment(value_num, bot_num))
            continue

        match = re.match(re_bot_to_output, line)
        if match:
            bot_num = int(match.group(1))
            low_target = match.group(2)
            low_target_num = int(match.group(3))
            high_target = match.group(4)
            high_target_num = int(match.group(5))
            expressions.append(Comparison(bot_num, low_target, low_target_num, high_target, high_target_num))                  

    return expressions

from queue import Queue

def examine_bots(expr: List[Expression], p1_values=[61,17], p2_chip_outputs=[0,1,2]):
    """
    Solves Part 1 and Part 2 simultaneously, by finding the inputs and outputs for each bot.
    Returns a pair (X,Y) where X is the solution for Part 1 (the bot number) and Y is the solution for Part 2 (the product of the chips).
    Params:
    * p1_values: list[int] - a list of chip values for Part 1 (the returned bot must compare ALL of these values).
    * p2_chip_outputs: list[int] - a list of the output lines for Part 2 (the product of the first value chip on each line will be returned).
    """

    value_to_bot = defaultdict(set)
    bot_inputs = defaultdict(set)
    bot_outputs = dict()
    chips_by_output = defaultdict(set)

    for exp in expr:
        if isinstance(exp, Assignment):
            value_to_bot[exp.value_num].add(exp.bot_num) 
            bot_inputs[exp.bot_num].add(exp.value_num)
        elif isinstance(exp, Comparison):
            bot_outputs[exp.bot_num] = BotOutputs(exp.low_is_bot, exp.low_target_num, exp.high_is_bot, exp.high_target_num)

    bots_to_check = Queue()
    for x in bot_outputs.keys():
        bots_to_check.put(x)

    ## Cycle exhaustively, passing inputs to outputs
    while not bots_to_check.empty():
        bot_num = bots_to_check.get()
        values = bot_inputs[bot_num]
        
        if len(values) < 2:
            ## Skip any bots that haven't got more than one input
            bots_to_check.put(bot_num)
            continue

        # print(f"Bot {bot_num} inputs: {values}")

        outputs = bot_outputs[bot_num]
        assert isinstance(outputs, BotOutputs) 
        low_val = min(values)
        high_val = max(values)

        if outputs.low_is_bot:
            # print(f"Bot {bot_num}: low ({low_val}) -> {outputs.low_num}")
            value_to_bot[low_val].add(outputs.low_num)
            bot_inputs[outputs.low_num].add(low_val)
        else:
            chips_by_output[outputs.low_num].add(low_val)

        if outputs.high_is_bot:
            # print(f"Bot {bot_num}: high ({high_val}) -> {outputs.high_num}")
            value_to_bot[high_val].add(outputs.high_num)
            bot_inputs[outputs.high_num].add(high_val)     
        else:
            chips_by_output[outputs.high_num].add(high_val)
 

    candidate_bots = set(bot_inputs.keys())
    for val in p1_values:
        ## Select all bots that receive this value as an input
        candidate_bots = candidate_bots.intersection(value_to_bot[val])
        # print(f"{candidate_bots} all compare {val}...")
        if len(candidate_bots) == 0:
            print("No solutions!")
            break

    p1_bot_num = None
    if len(candidate_bots) != 1:
        print(f"Warning: candidate bots was {candidate_bots}")
    else:
        p1_bot_num = list(candidate_bots)[0]
    
    ## Find the chips which are passed to the specific output lines
    p2_chip_product = 1
    for output in p2_chip_outputs:
        if len(chips_by_output[output]) != 1:
            print(f"Warning: output {output} has {len(chips_by_output[output])} chips")
        else:
            p2_chip_product *= list(chips_by_output[output])[0]

    return p1_bot_num, p2_chip_product




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    expressions = load(fname)
    targets = [5,2] if fname == 'example.txt' else [61,17]

    p1_bot_num, p2_chip_product = examine_bots(expressions, targets)
    print(f"Part one: {p1_bot_num}")    
    print(f"Part two: {p2_chip_product}")