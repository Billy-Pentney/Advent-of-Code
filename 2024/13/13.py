
import regex as re
import numpy as np

button_re = "X\+(\d+), Y\+(\d+)"
prize_line_re = "Prize: X=(\d+), Y=(\d+)"


def parse_nums(line, rgx):
    matches = re.findall(rgx, line)
    if len(matches) > 0:
        match = matches[0]
        return int(match[0]), int(match[1])


# def iterative_solve(a, b, prize):
#     ## Prize = i * a + j * b
#     ## p - i*a = j*b

#     p = np.array(prize)
#     A = np.array(a)
#     B = np.array(b)

#     pos = np.zeros(2)

#     b_pressed = int(np.min(p // B))
#     pos = b_pressed * B

#     while b_pressed > 0:
#         # One less press of button B
#         b_pressed -= 1
#         pos -= B
#         diff = p - pos

#         # Check if the remaining offset can be moved using button A only
#         if diff[0] % a[0] == 0 and diff[1] % a[1] == 0:
#             a_pressed = int(diff[0] // a[0])
#             return (a_pressed, b_pressed)
    
#     return None



def cramer(a,b,prize):
    p_x, p_y = prize[0],prize[1]
    a_x, a_y = a[0], a[1]
    b_x, b_y = b[0], b[1]

    ## Apply Cramer's rule
    A = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
    B = (a_x*p_y - a_y*p_x) / (a_x*b_y - a_y*b_x)

    ## Check for int solutions
    Aint = (A - int(A)) < 0.001
    Bint = (B - int(B)) < 0.001

    if Aint and Bint:
        return int(A),int(B)

    return None







def read_input(fname):
    machines = []
    with open(fname, "r") as file:
        machine = []
        for line in file.readlines():
            if len(machine) == 3:
                machines.append(machine)
                machine = []
            else:
                machine.append(line)
        if len(machine) == 3:
            machines.append(machine) 

    parsed_machines = []

    for machine in machines:
        a_line = machine[0]
        b_line = machine[1]
        prize_line = machine[2]
        button_a = parse_nums(a_line, button_re)
        button_b = parse_nums(b_line, button_re)
        prize = parse_nums(prize_line, prize_line_re)
        parsed_machines.append({ 'a': button_a,'b': button_b,'prize': prize })

    return parsed_machines



def compute_cost(machines):
    total_cost = 0

    COST_A = 3
    COST_B = 1

    for machine in machines:
        but_a = machine['a']
        but_b = machine['b']
        prize = machine['prize']
        presses = cramer(but_a, but_b, prize)

        print(f"A={but_a}, B={but_b}, Prize={prize}")

        if presses is None:
            print(" >> No Solution")
        else:
            (a_press, b_press) = presses

            cost = a_press * COST_A + b_press * COST_B
            print(f" >> ({a_press} x A) + ({b_press} x B) for cost = {cost}")

            total_cost += cost

    return total_cost



from sys import argv 



if __name__ == '__main__':

    fname = argv[1]
    input = read_input(fname)    
    part_1_total = compute_cost(input)

    print("-"*30)
    print(f"(Part 1) Total Cost: {part_1_total}")

    part_2_offset = [10000000000000,10000000000000]

    for machines in input:
        machines['prize'] = np.array(machines['prize']) + part_2_offset
    
    part_2_total = compute_cost(input)
    print("-"*30)
    print(f"(Part 2) Total Cost: {part_2_total}")
