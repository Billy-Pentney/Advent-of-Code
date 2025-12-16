import sys, os
import re


def read_file(fileaddr):
    lines = []
    with open(fileaddr, "r") as file:
        lines = file.readlines()

    ops = [parse_operation(line.strip("\n")) for line in lines]
    return ops


def to_int(nums):
    evald = []
    for num in nums:
        if num[0] in '0123456789':
            evald.append(int(num))
        else:
            evald.append(num)
    return evald


pattern_unary = re.compile("(NOT )?(\w+|\d+) -> (\w+)")
pattern_binary = re.compile("(\w+) (AND|OR) (\w+) -> (\w+)")
pattern_shift = re.compile("(\w+) (RSHIFT|LSHIFT) (\d+) -> (\w+)")

def parse_operation(line):
    unary_match = pattern_unary.match(line)
    if unary_match:
        apply_not = unary_match.group(1)
        input_name = unary_match.group(2)
        output_name = unary_match.group(3)
        op = None
        if apply_not is not None:
            op = 'NOT'
        return {'op': op, 'inputs': to_int([input_name]), 'output': output_name}
    
    binary_match = pattern_binary.match(line)
    if binary_match:
        input1 = binary_match.group(1)
        op = binary_match.group(2)
        input2 = binary_match.group(3)
        output_name = binary_match.group(4)
        return {'op': op, 'inputs': to_int([input1, input2]), 'output': output_name}
    
    shift_match = pattern_shift.match(line)
    if shift_match:
        input1 = shift_match.group(1)
        op = shift_match.group(2)
        input2 = shift_match.group(3)
        output_name = shift_match.group(4)
        return {'op': op, 'inputs': to_int([input1, input2]), 'output': output_name}

    return None



def evaluate_circuit(ops: list, states: dict, overrides={}):
    pending = ops

    # print("Running with states:", states)

    i = 0

    while len(pending) > 0:
        still_pending = []

        for action in pending:
            op = action['op']
            inputs = action['inputs']
            output = action['output']

            inputs_eval = []

            if output in overrides.keys():
                ## Override the first time this state is set
                states[output] = overrides[output]
                overrides.pop(output)
                continue

            ## Evaluate any wires
            for inpt in inputs:               
                if isinstance(inpt, str):
                    if inpt in states.keys():
                        inputs_eval.append(states[inpt]) 
                else:
                    inputs_eval.append(inpt)

            ## Check that all wires have values
            if len(inputs_eval) < len(inputs):
                still_pending.append(action)
                continue

            if op == 'NOT':
                states[output] = 65535 - inputs_eval[0]
            elif op == 'AND':
                states[output] = inputs_eval[0] & inputs_eval[1]
            elif op == 'OR':
                states[output] = inputs_eval[0] | inputs_eval[1]
            elif op == 'LSHIFT':
                states[output] = inputs_eval[0] << inputs_eval[1]
            elif op == 'RSHIFT':
                states[output] = inputs_eval[0] >> inputs_eval[1]
            elif op is None:
                states[output] = inputs_eval[0]
            else:
                print("Unknown operation:", op)

            if output in overrides:
                print(f"Set 'a' to {states[output]}")


        # print(len(still_pending))
        # print(states)
        pending = still_pending
        i+=1

    return states





if __name__ == '__main__':
    args = sys.argv[1:]
    filename = args[0]
    # part = args[1]
    fileaddr = os.path.dirname(os.path.realpath(sys.argv[0])) + "\\" + args[0]

    if not os.path.exists(fileaddr):
        print(f"Could not find file at location {fileaddr}")
        exit(1)

    ops = read_file(filename)

    evaluate_circuit_states = evaluate_circuit(ops, {})
    part_one_ans = evaluate_circuit_states.get('a', 0)
    print(f"(Part 1) Solution: {part_one_ans}")

    part_two_states = evaluate_circuit(ops, states={}, overrides={'b': part_one_ans})
    part_two_ans = part_two_states.get('a', 0)
    print(f"(Part 2) Solution: {part_two_ans}")
