
import numpy as np
import regex as re


## e.g. "y02 OR x01 -> tnw"
operation_re = re.compile("(\w+\d*) (XOR|AND|OR) (\w+\d*) -> (\w+\d*)")

## e.g. "y02: 1"
init_re = re.compile("(\w+\d*): (0|1)")



def load(fname):
    with open(fname, "r") as file:
        content = file.read()

    initialisations = {}
    operations = []

    for init_match in init_re.findall(content):
        var = init_match[0]
        value = int(init_match[1])
        initialisations[var] = value

    for op_match in operation_re.findall(content):
        first = op_match[0]
        op = op_match[1]
        second = op_match[2]
        result = op_match[3]
        operations.append((first, op, second, result))

    return initialisations, operations


def evaluate_z(inits, ops):
    state = inits.copy()

    remaining_ops = ops.copy()

    ## Slow, brute-force; iterate over the operations until they're all done
    while len(remaining_ops) > 0:
        expr = remaining_ops[0]
        remaining_ops = remaining_ops[1:]
        first, op, second, result = expr

        first_val = state.get(first, None)
        second_val = state.get(second, None)

        if first_val is None or second_val is None:
            remaining_ops.append(expr)
        else:
            if op == 'OR':
                state[result] = min(first_val + second_val, 1) 
            elif op == 'AND':
                state[result] = min(first_val * second_val, 1)
            elif op == 'XOR':
                state[result] = first_val ^ second_val
            else:
                print(f"Invalid operation: {op}")
        

    z_value = 0

    for var, val in state.items():
        if var.startswith('z') and val == 1:
            var_num = int(var[1:])
            value = int(pow(2,var_num))
            print(f"z_{var_num} = {value}")
            z_value += value
        
    return z_value





from sys import argv

if __name__ == '__main__':
    fname = argv[1]
    inits, ops = load(fname)
    print(inits.items())
    print(ops)

    z_value = evaluate_z(inits, ops)
    print(f"(Part 1) Z-Value: {z_value}")