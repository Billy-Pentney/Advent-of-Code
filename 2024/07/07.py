
import regex as re


eq_re = re.compile("(\d+):([ \d]+)")


def load(fname):
    with open(fname, "r") as file:
        content = file.readlines()

    equations = []

    for line in content:
        splits = line.strip("\n").split(": ")
        target = int(splits[0])
        nums = [int(x) for x in splits[1].split(" ")]
        equations.append((target, nums))

    return equations


def check_eq(current,nums,target,can_concat,indent="",verbose=False):

    if verbose:
        print(f"{indent}Have {current} with nums left: {nums}")

    if len(nums) == 0:
        if current == target:
            # print(f"{indent}Achieved {target}")
            return []
        else:
            return None
    
    # Early exit if we exceeded the target
    if current > target:
        return None

    plus = current + nums[0]

    trials = [(plus, '+')]

    if current > 0:
        times = current * nums[0]
        trials.append((times, '*'))
        if can_concat:
            concat = int(str(current) + str(nums[0])) 
            trials.append((concat, '||'))

    for new_curr, sym in trials:
        if verbose:
            print(f"{indent}{sym} {nums[0]}")
        suffix_ops = check_eq(new_curr, nums[1:], target, can_concat=can_concat, indent=indent+"   ")
        if suffix_ops is not None:
            x = [sym]
            if len(suffix_ops) > 0:
                x.extend(suffix_ops)
            return x
        
    return None


def intersperse(nums, ops):
    eq = []
    for num,op in zip(nums[:-1], ops):
        eq.append(num)
        eq.append(op)
    eq.append(nums[-1])
    return eq

def to_str(eq):
    return " ".join([str(x) for x in eq])


def eval_sum(eq):
    res = 0
    op = None
    for x in eq:
        if isinstance(x, str):
            op = x
        elif op == '+' or op is None:
            res += x
        elif op == '*':
            res *= x
        elif op == '||':
            res = int(str(res) + str(x))
    
    return res



def part_one(eqs, can_concat=False):
    valid_sum = 0

    for target,nums in eqs:
        eq_ops = check_eq(0, nums, target, can_concat=can_concat)

        if eq_ops is not None:
            valid_sum += target
            sum_with_ops = intersperse(nums, eq_ops[1:])
            sum_str = to_str(sum_with_ops)
            # evaluation = eval_sum(sum_with_ops)
            # print(f"Evaluation: {evaluation}")
            print(f"VALID: {target} = {sum_str}")
            # if evaluation != target:
            #     print(" >> ERROR")
        else:
            print(f"INVALID: {target} = {nums}")


    return valid_sum



from sys import argv

if __name__ == '__main__':

    fname = argv[1]
    equations = load(fname)
    # for target,nums in equations:
    #     print(f"Target={target}, Nums={nums}")

    sum_of_valid = part_one(equations)
    print(f"(Part 1) Sum of Valid Targets: {sum_of_valid}")

    print("\n","*"*30,"\n")

    sum_of_valid_with_concat = part_one(equations, can_concat=True)
    print(f"(Part 2) Sum of Valid Targets (w/ Concat): {sum_of_valid_with_concat}")
