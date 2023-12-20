import sys, os
import re


# G1 = x, G2 = m, G3 = a, G4 = s
part_pattern = "{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}"
class Part:
    def __init__(self, part_match):
        self.x = int(part_match.group(1))
        self.m = int(part_match.group(2))
        self.a = int(part_match.group(3))
        self.s = int(part_match.group(4))
        self.values = {
            'x': self.x,
            'm': self.m,
            'a': self.a,
            's': self.s
        }
    
    def sum_of_points(self):
        return self.x + self.m + self.a + self.s
    
    def get_attribute(self, var_name):
        if var_name in self.values.keys():
            return self.values[var_name]
        return None

    def __repr__(self):
        return f"(Part x={self.x}, m={self.m}, a={self.a}, s={self.s})"


# G1 = variable being compared
# G2 = Relation
# G3 = value to compare to 
# G4 = next workflow name
rule_pattern = "([asxm])([><=])(\d+):(\w+)"
rule_pattern_ungrouped = "[asxm][><=]\d+:\w+"

class Rule:
    def __init__(self, rule_match):
        self.target_var = rule_match.group(1)
        self.comp_op = rule_match.group(2)
        self.target_val = int(rule_match.group(3))
        self.next_workflow = rule_match.group(4)

    def compare_to_val(self, input_val):
        if self.comp_op == '<':
            return input_val < self.target_val
        elif self.comp_op == '>':
            return input_val > self.target_val
        # elif self.comp_op == '=':
        #     return input_val == self.target_val
        return False

    def accept_ranges(self, ranges):
        var_range = ranges[self.target_var]
        if self.comp_op == '>':
            ranges[self.target_var][0] = max(self.target_val+1, var_range[0])
        else: # '<'
            ranges[self.target_var][1] = min(self.target_val-1, var_range[1])
        return ranges

    def reject_ranges(self, ranges):
        var_range = ranges[self.target_var]
        if self.comp_op == '>':
            ranges[self.target_var][1] = min(self.target_val, var_range[1])
        else:
            ranges[self.target_var][0] = max(self.target_val, var_range[0])
        return ranges

    def matches(self, part: Part):
        part_val = part.get_attribute(self.target_var)
        return self.compare_to_val(part_val)

    def __repr__(self):
        return f"({self.target_var} {self.comp_op} {self.target_val})"



# G1 = name
# G2 = collection of rules
# G3 = final "catch" workflow
wf_pattern = f"(\w+){{({rule_pattern_ungrouped}(?:,{rule_pattern_ungrouped})*),(\w+)}}"

class Workflow:
    def __init__(self, wf_match):
        self.name = wf_match.group(1)
        self.rules = []
        self.catch_wf = wf_match.group(3)

        rules_raw = wf_match.group(2)
        for rule_raw in rules_raw.split(","):
            rule_match = re.match(rule_pattern, rule_raw)
            if rule_match:
                self.rules.append(Rule(rule_match))

    def run_on_part(self, part: Part):
        for rule in self.rules:
            if rule.matches(part):
                return rule.next_workflow
        
        return self.catch_wf

    def __repr__(self):
        return f"({self.name}: rules={self.rules}, final={self.catch_wf})"



def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    workflows = {}
    parts = []

    mode = 1

    for line in lines:
        if mode == 1:
            wf_match = re.match(wf_pattern, line)
            print(line)
            if wf_match:
                wf = Workflow(wf_match)
                workflows[wf.name] = wf
            else:
                mode = 2
        
        if mode == 2:
            part_match = re.match(part_pattern, line)
            if part_match:
                parts.append(Part(part_match)) 

    return workflows, parts




## Solve Part One
def part_one(fileaddr):
    wfs, parts = read_file(fileaddr)

    # Sum the total ratings of each part that's accepted
    sum_acc_parts = 0

    for part in parts:
        wf_name = 'in'

        # Run each part through the machine till termination
        while wf_name != 'A' and wf_name != 'R':
            wf = wfs[wf_name]
            wf_name = wf.run_on_part(part)

        if wf_name == 'A':
            sum_acc_parts += part.sum_of_points()
            # print(f"Accepted: {part}")

    return sum_acc_parts


def count_combs_of_ranges(ranges):
    combs = 1
    for range_val in ranges.values():
        range = range_val[1]+1 - range_val[0]
        combs *= max(0, range)
    return combs

def copy_dict(d):
    d_copy = {}
    for key, val in d.items():
        d_copy[key] = val.copy()
    return d_copy


def find_wf_proportion_accepted(wfs, wf_name, ranges):
    if wf_name == 'A':
        return count_combs_of_ranges(ranges)
    elif wf_name == 'R':
        return 0

    wf = wfs[wf_name]

    accepted = 0
    # all_possible = count_combs_of_ranges(ranges)

    for rule in wf.rules:
        ranges_acc = rule.accept_ranges(copy_dict(ranges))
        ranges_rej = rule.reject_ranges(copy_dict(ranges))

        print(f"Applying rule {rule} to get acc: {ranges_acc}")

        if rule.next_workflow == 'A':
            accepted += count_combs_of_ranges(ranges_acc)
        elif rule.next_workflow != 'R':
            accepted += find_wf_proportion_accepted(wfs, rule.next_workflow, ranges_acc)     

        ranges = ranges_rej

        for val in ranges.values():
            # No valid values for this range
            if val[1] < val[0]:
                return accepted        

    return accepted + find_wf_proportion_accepted(wfs, wf.catch_wf, ranges)



## Solve Part Two
def part_two(fileaddr):
    wfs, _ = read_file(fileaddr)
    ranges = {
        'x': [1,4000],
        'm': [1,4000],
        'a': [1,4000],
        's': [1,4000]
    }

    return find_wf_proportion_accepted(wfs, 'in', ranges)










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
    
