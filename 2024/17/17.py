
import regex as re

init_register_re = re.compile('Register ([A-C]): (\d+)\n?') 
init_program_re = re.compile('Program: ([\d,]+)\n?') 

def load(fname):
    with open(fname, "r") as file:
        lines = file.readlines()

    registers = {}
    program = []

    for line in lines:
        reg_match = init_register_re.match(line)
        prog_match = init_program_re.match(line)
        if reg_match:
            register = reg_match[1]
            registers[register] = int(reg_match[2])
        elif prog_match:
            instructions = prog_match[1]
            program = [int(it) for it in instructions.split(",")]

    return registers, program



def decode_operand(opr, a, b, c):
    """
        Combo operands 0 through 3 represent literal values 0 through 3.
        Combo operand 4 represents the value of register A.
        Combo operand 5 represents the value of register B.
        Combo operand 6 represents the value of register C.
        Combo operand 7 is reserved and will not appear in valid programs.
    """
    if opr >= 0 and opr <= 3:
        return opr
    elif opr == 4:
        return a
    elif opr == 5:
        return b
    elif opr == 6:
        return c
    else:
        print("Invalid program")
        return None



def run(registers, program, verbose=True, quine_search=False):

    a = registers['A']
    b = registers['B']
    c = registers['C']

    n = len(program)

    outputs = []

    ## Instruction pointer
    i = 0

    executions = 0
    max_exec = 10000

    while i < n:

        if executions >= max_exec:
            # print("Execution limit reached!")
            break 

        executions += 1
        opcode = program[i]
        operand = program[i+1]
        eval_opr = decode_operand(operand, a, b, c) 

        # print(f"Opcode={opcode}, operand={eval_opr}")

        if opcode == 0:
            ## ADV
            ## A = A / 2^eval(operand)
            op = 'ADV'
            a = a // pow(2, eval_opr)

        elif opcode == 1:
            ## BXL
            ## B = B XOR literal(operand)
            op = "BXL"
            b = b ^ operand

        elif opcode == 2:
            ## BST
            ## B = eval(operand) % 8
            op = "BST"
            b = eval_opr % 8 

        elif opcode == 3:
            ## JNZ
            ## Jump if non-zero
            op = "JNZ"
            if a != 0:
                # Jump to literal of operand
                i = operand
                ## DO NOT INCREASE THE INSTRUCTION POINTER
                continue
            
        elif opcode == 4:
            op = "BXC"
            b = b ^ c

        elif opcode == 5:
            op = "OUT"
            ## OUT
            ## Output the combo operand
            outputs.append(eval_opr % 8)

            if quine_search:
                out_i = len(outputs)-1
                # Check that the program is outputting itself
                if out_i >= len(program) or outputs[-1] != program[out_i]:
                    return outputs

        elif opcode == 6:
            ## BDV
            op = "BDV"
            b = a // pow(2, eval_opr)

        elif opcode == 7:
            ## CDV
            op = "CDV"
            c = a // pow(2, eval_opr)

        if verbose:
            print(f"{op}({operand})")
            print(f"A = {a}, B = {b}, C = {c}")

        i += 2

    return ",".join([str(o) for o in outputs])


def brute_force_part_two(regs, prog, start=0, end=10000, interval=100):
    for a in range(start,end):
        regs['A'] = a
        output = run(regs, prog, verbose=False, quine_search=True)
        if a % interval == 0:
            print(str(a))
        if output == ",".join([str(x) for x in prog]):
            return a
    
    return -1




from sys import argv

if __name__ == '__main__':
    fname = argv[1]

    regs, prog = load(fname)
    print(regs)
    print(prog)

    execution_result = run(regs, prog)
    print(f"(Part 1) Result: {execution_result}")

    min_a = brute_force_part_two(regs, prog, start=int(1e7), end=int(1e8), interval=100000)
    print(f"(Part 2) Minimum A for loop: {min_a}")
